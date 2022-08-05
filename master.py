from importlib.resources import path
import os 
from os import get_inheritable, listdir
from re import X
import pandas as pd
import geopandas as gpd
import configparser
import rasterio 
from rasterio.mask import mask
from rasterio.warp import reproject, calculate_default_transform
from rasterio.merge import merge
import rasterio.crs
import json
import fiona
import rasterstats
from rasterstats import zonal_stats
import numpy as np
from shutil import copyfile
from osgeo import gdal
import glob
import subprocess
from PIL import Image
import glob
import rioxarray 
import georasters 
import csv
import shapely
from shapely.geometry import Point, LineString, Polygon, MultiPolygon, shape, mapping, box 
import pyproj

from misc import countries


CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')

DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')


def countries():                                    # CREATES DICTIONRY OF COUNTRIES
    """
    This function produces country information.

    Returns
    -------
    countries : list of dicts
        Contains all desired country information for countries in
        the stated continent.
    
    """

    # print('Adding continent information to country shapes')
    glob_info_path = os.path.join(BASE_PATH, 'raw', 'countries.csv')
    global_info = pd.read_csv(glob_info_path, encoding = "ISO-8859-1",
        keep_default_na=False)
   
    countries = []

    for index, country in global_info.iterrows():

        if country['exclude'] == 1:
            continue 

        countries.append({
            'country_name': country['country'],
            'iso3': country['iso3'],
            'iso2': country['iso2'],
            'gid_region': country['gid_region'],
            'region': country['continent'],
            'exclude': country['exclude'],
            'lowest':country['lowest'], #### NEW
            'continent':country['continent'], ###### NEW2
            'world_bank_region': country['wb_regional_group'],  #####NEW2
            'world_bank_income': country['wb_income_group'],    ######NEW2

        })

    return countries


def area_of_polygon(geom):                          # GET ARE OF POLYGON IN KM2
    """
    Returns the area of a polygon. Assume WGS84 as crs.
    """
    geod = pyproj.Geod(ellps="WGS84")

    poly_area, poly_perimeter = geod.geometry_area_perimeter(
        geom
    )

    return abs(poly_area)


def hdf_tif_reproj(year):                           # CONVERTS HDF4 TO TIFF AND SETS PROJECTION TO EPSG:4326
    """
    Extracts data as tif from land cover HDF file
    """
    
    # Define a folder for output 
    converted_tifs_path = os.path.join(DATA_INTERMEDIATE, 'land_cover_{}'.format(year))
    
    if os.path.exists(converted_tifs_path):
        print('folder exists')
    if not os.path.exists((converted_tifs_path)):
        os.makedirs((converted_tifs_path))
        print('Land Cover folder created for {}'.format(year))
    
    # Define gdal transform command 
    basecmd = 'gdal_translate -of GTiff -a_srs "+init=epsg:4326" -a_ullr -180 90 180 -90 -co "COMPRESS=PACKBITS"'
    # Link to land cover HDF datasets
    land_hdf = os.path.join(DATA_RAW, 'modis', '{}.01.01'.format(year))

    # Append HDF files in folder to a list 
    land_files = []
    os.chdir(land_hdf)

    for file in glob.glob('*.hdf'):
        land_files.append(os.path.abspath(os.path.join(file)))

    # Create List to store Desired SDS 'LC_Type1'
    lc_type1_files = []

    # Open HDF files 
    for file in land_files:
        hdf_open = gdal.Open(file)
        
        # Viewing SubDatasets for Each file, print desired SDS type
        sds_list = hdf_open.GetSubDatasets()
        #print(sds_list[0])

        # Append Desired data to list
        lc_type1_files.append(sds_list[0])

        # Previous list includes data type so remove 
        lc_list = [x[0] for x in lc_type1_files]   
        

        for x in lc_list:
            PROJ4 = '+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs'
            kwargs = {'format':'Gtiff', 'srcSRS': PROJ4 , 'dstSRS':'EPSG:4326'}
        gdal.Warp(destNameOrDestDS = '{}_{}.tiff'.format(x[91:97],year), srcDSOrSrcDSTab = '{}'.format(x[0:137]), **kwargs) 


def process_country_shapes(country):                # WRITE NATIONAL BOUNDRY SHAPEFILES OUT
    """
    Creates a single national boundary for the desired country.
    Parameters
    ----------
    country : dict
        Contains all desired country information.

    """
    iso3 = country['iso3']

    # path = os.path.join(DATA_RAW, iso3)
    my_new_path = os.path.join(DATA_INTERMEDIATE, iso3)
    path_out = os.path.join(my_new_path, 'national_outline.shp')

    if os.path.exists(path_out):
        print('Completed national outline processing')

    if not os.path.exists(my_new_path):
        os.makedirs(my_new_path)

    path = os.path.join(DATA_RAW, 'gadm36_levels_shp', 'gadm36_0.shp')
    countries = gpd.read_file(path)

    single_country = countries[countries.GID_0 == iso3].reset_index()

    # # if not iso3 == 'MDV':
    # single_country['geometry'] = single_country.apply(
    #     remove_small_shapes, axis=1)

    print('Adding ISO country code and other global information')
    glob_info_path = os.path.join(DATA_RAW, 'countries.csv')
    load_glob_info = pd.read_csv(glob_info_path, encoding = "ISO-8859-1",
        keep_default_na=False)
    single_country = single_country.merge(
        load_glob_info, left_on='GID_0', right_on='iso3')

    # print('Exporting processed country shape')
    single_country.to_file(path_out, driver='ESRI Shapefile')

    return print('National Boundry Shapefile for {} Written!'.format(iso3))


def process_region_shapes(country):                 # WRITE REGIONAL BOUNDRY SHAPEFILES OUT
    """
    Function for processing the lowest desired subnational
    regions for the chosen country.
    Parameters
    ----------
    country : dict
        Contains all desired country information.
    """
    regions = []
    print(country)

    iso3 = country['iso3']
    level = country['lowest'] # changed from 'gid_region'
    #level = country['gid_region']

    for regional_level in range(1, level + 1):

        filename = 'regions_{}_{}.shp'.format(regional_level, iso3)
        folder = os.path.join(DATA_INTERMEDIATE, iso3, 'regions')  # CHANGED FROM RAW TO INT
        path_processed = os.path.join(folder, filename)

        if os.path.exists(path_processed):
            continue

        print('Working on {} level {}'.format(iso3, regional_level))

        if not os.path.exists(folder):
            os.mkdir(folder)

        filename = 'gadm36_{}.shp'.format(regional_level)
        path_regions = os.path.join(DATA_RAW, 'gadm36_levels_shp', filename)

        path_regions = os.path.join(DATA_RAW, 'gadm36_levels_shp', 'gadm36_2.shp')
        regions = gpd.read_file(path_regions)
        regions = regions[regions.GID_0 == iso3]

    #     # # print('Excluding small shapes')
    #     # regions['geometry'] = regions.apply(remove_small_shapes, axis=1)

        try:
            # print('Writing global_regions.shp to file')
            regions.to_file(path_processed, driver='ESRI Shapefile')
        except:
            # print('Unable to write {}'.format(filename))
            pass

    print('Completed processing of regional shapes level {}'.format(level))

    return print('Regional Shapefiles for {} Written!'.format(iso3))


def clip_gdp_to_national_boundary(country, year):   # CLIP GDP LAYER TO NATIONAL BOUNDRY
    """
    Take a .tiff global file and export for a country.

    Parameters
    ----------
    country : string
        Three digit ISO country code.
    file : string
        Path to master global file.

    """
    iso3 = country['iso3']

    # Path to GDP tiff for a given year
    path_gdp = os.path.join(DATA_INTERMEDIATE, 'gdp_5arc_{}.tiff'.format(year))
    if os.path.exists(path_gdp):
        settlements = rasterio.open(path_gdp, 'r+')
        settlements.nodata = 255
        settlements.crs = {"init": "epsg:4326"} 
    if not os.path.exists(path_gdp):
        print('No GDP.Tiff for {} found'.format(year))
    
    # Path to national Shapefile 
    iso3 = country['iso3']
    path_country = os.path.join(DATA_INTERMEDIATE, iso3, 'national_outline.shp')

    if os.path.exists(path_country):
        country_shape = gpd.read_file(path_country)
    else:
        print('Must generate national_outline.shp first' )

    # Reread bounds of shapefile 
    with fiona.open(path_country, 'r') as shapefile:
        shapes = [feature['geometry'] for feature in shapefile]

    # Reread bounds of TIFF 
    with rasterio.open(path_gdp) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop = True)
        out_meta = src.meta

    # Update metadata for clipped gdp tiff 
    out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform,
                 "crs": "EPSG:4326"
                 })

    # Define folder for outputting regional GDP 
    path_out = os.path.join(DATA_INTERMEDIATE, iso3, 'GDP')
    if os.path.exists(path_out):
        print('GDP folder for {} exists'.format(iso3))
    if not os.path.exists(path_out):
        os.makedirs(path_out)

    file_out = os.path.join(path_out, 'gdp_5arc_{}_{}.tiff'.format(iso3,year))

    with rasterio.open(file_out, 'w+', **out_meta) as dest:
        dest.write(out_image)
        print('GDP clipped to {} for {}!'.format(iso3,year))


def clip_population_tiff(country,year):             # CLIP POPULATION LAYER TO NATIONAL BOUNDRY
    """
    This Script Clips the Global Population Tiff By unprojected National raster.
    Population Raster is too large to reproject  
    """
    iso3 = country['iso3']

    # Link to Global Population Tiff 
    tiff_path = os.path.join(DATA_RAW, 'ppp_{}_1km_Aggregated.tif'.format(year))
    pop_tiff = rasterio.open(tiff_path)

    # Link to Shapefile 
    path_country = os.path.join(DATA_INTERMEDIATE, iso3, 'national_outline.shp')
    country_shape = gpd.read_file(path_country)

    # Check CRS of Tiff and Shapefile 
    print(pop_tiff.crs, 'TIFF CRS')
    print(country_shape.crs, 'SHAPE CRS')

    # Reread bounds of shapefile 
    with fiona.open(path_country, 'r') as shapefile:
        shapes = [feature['geometry'] for feature in shapefile]

    # Reread bounds of TIFF 
    with rasterio.open(tiff_path) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop = True)
        out_meta = src.meta

    # Update metadata for clipped gdp tiff 
    out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform
                 })

    # Create Folder to store Population Data 
    folder_out = os.path.join(DATA_INTERMEDIATE, iso3, 'Population')
    if os.path.exists(folder_out):
        print('Population folder for {} Exists'.format(iso3))
    else:
        os.makedirs(folder_out)

    # Write Image out 
    file_out = os.path.join(folder_out, 'population_{}_{}.tiff'.format(iso3,year))

    with rasterio.open(file_out, 'w+', **out_meta) as dest:
        dest.write(out_image)
        print('Population clipped to {} for {}!'.format(iso3,year))


def find_correct_raster_tile(country, year):        # FINDS LC RASTERS THAT INTERSECT NATIONAL BOUNDING BOX, AND OUTPUTS MOSAICED TIFF
    """
    Parameters
    ----------
    polygon : tuple
        The bounds of the modeling region.
    tile_lookup : dict
        A lookup table containing raster tile boundary coordinates
        as the keys, and the file paths as the values.
    Return
    ------
    output : list
        Contains the file path to the correct raster tile. Note:
        only the first element is returned and if there are more than
        one paths, an error is returned.
    """
    iso3 = country['iso3'] 

    # Link to National Shapefile 
    path_national = os.path.join(DATA_INTERMEDIATE, iso3, 'national_outline.shp') 

    if os.path.exists(path_national):
        polygon = gpd.read_file(path_national)
    else:
        print('Must Generate National Shapefile first')

    # Get Bounding Box of Shapefile 
    poly_bounds = polygon['geometry'].total_bounds 
    poly_bbox = box(*poly_bounds, ccw = False)   #output order= lrc, urc, ulc, llc 

    # Link to Land Cover Data 
    path_lc = os.path.join(DATA_RAW, 'modis', '{}.01.01'.format(year))

    land_files = [os.path.abspath(os.path.join(path_lc, f)) for f in os.listdir(path_lc) if f.endswith('.tiff')]
    
    # Create List to Store Intersecting tiles 
    intersections_paths = []
    
    # Get Bounds of each Tiff
    for land_file in land_files:
        path = os.path.join(path_lc, land_file)
        read_files = rasterio.open(path, 'r+')

        tiff_bounds = read_files.bounds
        tiff_bbox = box(*tiff_bounds)

        # Check if any bounds are intersected 
        if tiff_bbox.intersects(poly_bbox):
            intersections_paths.append(land_file)
    
    
    print(intersections_paths, 'og')

    # Move first item of list to end, in case 'edges' appear in interactions, done to preserve resolution 
    intersections_paths += [intersections_paths.pop(0)]
    print(intersections_paths, 'mod')

    # Link to path to store the merged Raster we'll Create 
    merged_raster_path = os.path.join(DATA_INTERMEDIATE, iso3, 'land_cover_data')
    
    if os.path.exists(merged_raster_path):
        print('Folder to store Rasters Exists')
    if not os.path.exists(merged_raster_path):
        os.makedirs(merged_raster_path)

    # Merge the intersecting Rasters Together
    raster_to_mosaic = []
    for x in intersections_paths:
        raster = rasterio.open(x)
        raster_to_mosaic.append(raster)
    
    print(raster_to_mosaic)
    
    mosaic, output = merge(raster_to_mosaic)
    
    # Update Metadata for export 

    output_meta = raster.meta.copy()
    output_meta.update({
        'name':'Merged_Raster_{}_{}'.format(iso3, year), 
        'driver' :'GTiff',
        'height': mosaic.shape[1],
        'width': mosaic.shape[2],
        'crs':read_files.profile['crs'],
        'compress':'lzw',
        'transform': output
        })
   
    # Add file name for output 
    mosaic_path = os.path.join(merged_raster_path, 'merged_LC_{}_{}.tiff'.format(iso3, year))
    
    # Write The Raster out 
    with rasterio.open(mosaic_path, 'w+', **output_meta) as m:
        m.write(mosaic)
        print('Mosaicd Land Cover Tiff Created for {}'.format(iso3))


def lc_mosaic_clipper(country, year):               # CLIPS MOSAICED LAND COVER TIFF TO NATIONAL BOUNDRYS
    """
    This script will clip the mosaics created in 'find_correct_raster_tile'
    """

    iso3 = country['iso3']

    # Link To Shapefile 
    path_national = os.path.join(DATA_INTERMEDIATE, iso3, 'national_outline.shp') 

    if os.path.exists(path_national):
        polygon = gpd.read_file(path_national)
    else:
        print('Must Generate National Shapefile first')

    # Link to Mosaic Tiff 
    mosaic_path = os.path.join(DATA_INTERMEDIATE, iso3, 'land_cover_data', 'merged_LC_{}_{}.tiff'.format(iso3, year))

    if os.path.exists(mosaic_path):
        mosaic = rasterio.open(mosaic_path)
    else:
        print('No Mosaic for {} exists!'.format(iso3))

    # Check CRS of Each File 
    print(polygon.crs, 'shapefile crs')
    print(mosaic.crs, 'mosaic crs')

    # Re Read shapefile with fiona to store its geometry 
    with fiona.open(path_national, 'r') as shapefile:
        shapes = [feature['geometry'] for feature in shapefile]

    # Re Read TIFF
    with rasterio.open(mosaic_path) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop = True)
        out_meta = src.meta

    # Update Clipped RAsters Metadata 
    out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform
                 })

    # Define name and path for clipped tiff 
    clipped_path = os.path.join(DATA_INTERMEDIATE, iso3, 'land_cover_data', 'clipped_LC_{}_{}.tiff'.format(iso3, year))

    with rasterio.open(clipped_path, 'w+', **out_meta) as dest:
        dest.write(out_image)
        print('Mosaic for {} Clipped to National Bounds!'.format(iso3))


def scaled_mean(x):
    """
    Custom Statistic to return Mean rescaled for NETCDF
    """
    #scaled_mean = np.ma.mean(x) * ((np.subtract(np.ma.max(x) ,np.ma.min(x)) / 4294967295))
    scaled_mean = np.ma.mean(x) / (65535)
    return scaled_mean


def scaled_median(x):
    """
    Custom Statistic to return Sum rescaled for NETCDF
    """
    scaled_sum = (np.ma.median(x)) * (1/65535)
    return scaled_median


def scaled_sum(x):
    """
    Custom Statistic to return Sum rescaled for NETCDF
    """
    scaled_sum = np.ma.sum(x) / (65535)
    return scaled_sum


def subregion_stats(country,year):               # EXTRACTING STATS FOR GDP, POP, LC AND WRITING OUT TO CSV
    """
    This script outputs csvs containg landcover and gdp stats for each region in a country
    """
    
    # Link to Countries CSV 
    countries_csv = os.path.join(DATA_RAW, 'countries.csv')
    countries_read = pd.read_csv(countries_csv, encoding = 'latin-1')
    
    level = country['lowest']
    iso3 = country['iso3']
    continent = country['continent']
    # world_bank_region = country['wb_regional_group']
    # world_bank_income = country['wb_income_group']

    # Link to Regional Shapefile 
    region_path = os.path.join(DATA_INTERMEDIATE, iso3, 'regions', 'regions_{}_{}.shp'.format(level, iso3))
    if os.path.exists(region_path):
        regions = gpd.read_file(region_path)
    else: 
        print('must generate regions first')

    # Link to GDP Data 
    gdp_path = os.path.join(DATA_INTERMEDIATE, iso3, 'gdp', 'gdp_5arc_{}_{}.tiff'.format(iso3, year))
    with rasterio.open(gdp_path) as srb:
        gdp_affine = srb.transform
        gdp_array = srb.read(1)
        print(srb.crs, 'GDP CRS')

    # Link to Population Data 
    pop_path = os.path.join(DATA_INTERMEDIATE, iso3, 'Population', 'population_{}_{}.tiff'.format(iso3,year))
    with rasterio.open(pop_path) as src:
        pop_affine = src.transform
        pop_array = src.read(1)
        print(src.crs, 'POPULATION CRS')

    # Link to Clipped Land Cover Data
    lc_tiff_path = os.path.join(DATA_INTERMEDIATE, iso3, 'land_cover_data', 'clipped_LC_{}_{}.tiff'.format(iso3, year))
    with rasterio.open(lc_tiff_path) as srd:
        lc_affine = srd.transform
        lc_array = srd.read(1)
        print(srd.crs, 'LAND COVER CRS')

    # Define Categories for Land Cover Dataset 
    cmap = {1:'Evergreen Needleleaf', 2:'Evergreen Broadleaf', 3:'Deciduous Needleleaf', 4:'Deciduous Broadleaf', 5:'Mixed Forest',
    6:'Closed Shrubland', 7:'Open Shrubland', 8:'Woody Savanas', 9:'Savanas', 10:'Grasslands',
    11:'Permanant Wet Lands', 12:'Croplands', 13:'Urban and Built Up Lands', 14:'Croplands/Natural Vegetation Mosaics',
    15:'Permanant Snow and Ice', 16:'Barren', 17:'Water'}

    # Define Path Out
    path_out = os.path.join(DATA_INTERMEDIATE, iso3, 'stats')
    if os.path.exists(path_out):
        print('Stats folder for {} Exists'.format(iso3))
    
    if not os.path.exists(path_out):
        os.makedirs(path_out)

    results = []
    for index, region in regions.iterrows():
        with rasterio.open(gdp_path) as srb:
        
            identifier = region['GID_{}'.format(level)]

            affine = srb.transform
            array = srb.read(1)

            gdp_stats = rasterstats.zonal_stats(
                region['geometry'], 
                array, 
                affine = affine, 
                stats = ['count', 'sum', 'mean'], 
                add_stats = {'scaled_mean':scaled_mean, 'scaled_sum':scaled_sum, 'scaled_median':scaled_median},
                geojson_out= False, 
                all_touched = False
            
            )[0]
    

        with rasterio.open(pop_path) as src:

            affine = src.transform
            array = src.read(1)

            ndval = src.nodatavals[0]
            array[array==ndval] = np.nan

            pop_stats = rasterstats.zonal_stats(
                region['geometry'],
                array,
                affine = affine,
                stats = ['sum'],
                geojson_out = False,
                nodata= 0,
            )[0]



        with rasterio.open(lc_tiff_path) as srd:

            affine = srd.transform
            array = srd.read(1)

            lc_stats = rasterstats.zonal_stats(
                region['geometry'], 
                array, 
                affine = affine, 
                stats = ['unique', 'majority', 'count'], 
                geojson_out= False, 
                categorical = True, 
                category_map = cmap
                )[0]

            if 'Evergreen Needleleaf' in lc_stats:
                    evergreen_needleleaf = lc_stats['Evergreen Needleleaf']
            else:
                    evergreen_needleleaf = 0

            if 'Evergreen Broadleaf' in lc_stats:
                    evergreen_broadleaf = lc_stats['Evergreen Broadleaf']
            else:
                    evergreen_broadleaf = 0 

            if 'Deciduous Needleleaf' in lc_stats:
                    decidous_needleleaf = lc_stats['Deciduous Needleleaf']
            else:
                    decidous_needleleaf = 0

            if 'Deciduous Broadleaf' in lc_stats:
                    deciduous_broadleaf = lc_stats['Deciduous Broadleaf']
            else:
                    deciduous_broadleaf = 0

            if 'Mixed Forest' in lc_stats:
                    mixed_forest = lc_stats['Mixed Forest']
            else:
                    mixed_forest = 0

            if 'Closed Shrubland' in lc_stats:
                    closed_shrubland = lc_stats['Closed Shrubland']
            else:
                    closed_shrubland = 0

            if 'Open Shrubland' in lc_stats:
                    open_shrubland = lc_stats['Open Shrubland']
            else:
                    open_shrubland = 0

            if 'Woody Savanas' in lc_stats:
                    woody_savanas = lc_stats['Woody Savanas']
            else:
                    woody_savanas = 0

            if 'Savanas' in lc_stats:
                    savanas = lc_stats['Savanas']
            else:
                    savanas = 0

            if 'Grasslands' in lc_stats:
                    grasslands = lc_stats['Grasslands']
            else:
                    grasslands = 0

            if 'Permanant Wet Lands' in lc_stats:
                    perm_wet_lands = lc_stats['Permanant Wet Lands']
            else:
                    perm_wet_lands = 0

            if 'Croplands' in lc_stats:
                    croplands = lc_stats['Croplands']
            else:
                    croplands = 0

            if 'Urban and Built Up Lands' in lc_stats:
                    urban_built_lands = lc_stats['Urban and Built Up Lands']
            else:
                    urban_built_lands = 0

            if 'Croplands/Natural Vegetation Mosaics' in lc_stats:
                    crop_nat_veg_mos = lc_stats['Croplands/Natural Vegetation Mosaics']
            else:
                    crop_nat_veg_mos = 0

            if 'Permanant Snow and Ice' in lc_stats:
                    perm_snow_ice = lc_stats['Permanant Snow and Ice']
            else:
                    perm_snow_ice = 0

            if 'Barren' in lc_stats:
                    barren = lc_stats['Barren']
            else:
                    barren = 0

            if 'Water' in lc_stats:
                    water = lc_stats['Water']
            else:
                    water = 0

            if lc_stats['count'] == 0:
                continue
            
            area_km2 = round(area_of_polygon(region['geometry']) / 1e6)
            if area_km2 == 0:
                continue



        results.append({
                'Country': region['NAME_0'], #changed all regions to region
                'GID_0': region['GID_0'],
                'GID_ID': region['GID_2'],
                'Area km2': area_km2, 
                'GID_Level': level,
                'Population':pop_stats['sum'],
                'unique_lc_stats': lc_stats['unique'],
                'majority_lc_stats': lc_stats['majority'],
                'total_pixel_lc_count': lc_stats['count'],
                'lc_area_pixel_factor': lc_stats['count'] / area_km2,
                'scaled_mean_gdp': gdp_stats['scaled_mean'],
                'scaled_gdp_sum': gdp_stats['scaled_sum'],
                'scaled_gdp_sum': gdp_stats['scaled_sum'],
                'gdp_count':gdp_stats['count'],
                'gdp_sum': gdp_stats['sum'],
                'gdp_mean': gdp_stats['mean'],
                'Evergreen_Needleleaf': evergreen_needleleaf * (area_km2 / lc_stats['count']),
                'Evergreen_Broadleaf': evergreen_broadleaf * (area_km2 / lc_stats['count']),
                'Decidous_Needleleaf': decidous_needleleaf * (area_km2 / lc_stats['count']),
                'Deciduous_Broadleaf': deciduous_broadleaf * (area_km2 / lc_stats['count']),
                'Mixed_Forest' : mixed_forest * (area_km2 / lc_stats['count']),
                'Closed_Shrubland': closed_shrubland * (area_km2 / lc_stats['count']),
                'Open_Shrubland': open_shrubland * (area_km2 / lc_stats['count']),
                'Woody_Savanas': woody_savanas* (area_km2 / lc_stats['count']),
                'Savanas': savanas* (area_km2 / lc_stats['count']),
                'Grasslands': grasslands* (area_km2 / lc_stats['count']),
                'Permanant_Wet_Lands': perm_wet_lands* (area_km2 / lc_stats['count']),
                'Croplands': croplands* (area_km2 / lc_stats['count']), 
                'Urban_and_Built_Up_Lands': urban_built_lands* (area_km2 / lc_stats['count']),
                'Croplands_or_Natural_Vegetation_Mosaics': crop_nat_veg_mos* (area_km2 / lc_stats['count']),
                'Permanant_Snow_and_Ice': perm_snow_ice* (area_km2 / lc_stats['count']),
                'Barren': barren* (area_km2 / lc_stats['count']),
                'Water': water* (area_km2 / lc_stats['count']),
                'Continent': continent,
                'World_Bank_Regions': country['world_bank_region'],
                'World_Bank_Income': country['world_bank_income'],
                'Year': year
                })  

    
    results_df = pd.DataFrame(results)
    path_output = os.path.join(path_out,  'stats_{}_{}_OG.csv'.format(iso3,year)) 
    results_df.to_csv(path_output, index=False)


    path_output2 = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', '{}'.format(year), 'stats_{}_{}_OG.csv'.format(iso3,year))
    results_df.to_csv(path_output2, index=False)
    #outfile = os.path.join(DATA_INTERMEDIATE, iso3, 'stats', '{}_stats.csv'.format(identifier))
    
    print('MY MOMMA RAISED ME A PROPHET, I PLAY FOR DOLLAR INCENTIVE')


# hdf_tif_reproj(2005)

if __name__ == '__main__':

    for country in countries():        

        # if not country['iso3'] in ['ETH','SYR', 'SOM', 'TJK', 'UGA', 
        #                         'NGA', 'PAK', 'KGZ', 'HND', 'BTN',
        #                         'MYS', 'BLR','CRI', 'AZE', 'BGR', 
        #                         'NLD', 'PAN', 'HRV', 'PRT', 'CHE']:
        #     continue
        
        if not country['iso3'] == 'HND':
            continue


        year = 2005

        # # # # -------------------- SHAPEFILE EXTRACTION FUNCTIONS ---------------------------------
        # process_country_shapes(country)
        # process_region_shapes(country)

        # # # # -------------------- CLIPPING GLOBAL DATASETS ---------------------------------------
        clip_gdp_to_national_boundary(country, year)
        clip_population_tiff(country, year)

        # # # # -------------------- LAND COVER FUNCTIONS -------------------------------------------
        find_correct_raster_tile(country,year)
        lc_mosaic_clipper(country,year)

        # # # # -------------------- DOLLAR INCENTIVE -----------------------------------------------
        subregion_stats(country,year)