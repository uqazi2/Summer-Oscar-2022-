import xarray 
import rioxarray 
import configparser
import os
import netCDF4 as nc
import rasterio as rio

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')

DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')

def ncf_to_tiff():

    # Link to NCF file
    ncf_path = os.path.join(DATA_RAW, 'doi_10.5061_dryad.dk1j0__v2', 'GDP_per_capita_PPP_1990_2015_v2.nc')

    # Open NCF
    nc_file = xarray.open_dataset(ncf_path)


# Link to NCF file
ncf_path = os.path.join(DATA_RAW, 'doi_10.5061_dryad.dk1j0__v2', 'GDP_PPP_1990_2015_5arcmin_v2.nc')

nc_file = nc.Dataset(ncf_path, 'r')
print(nc_file)

print(nc_file.variables.keys())

gdp_ppp = nc_file.variables['GDP_PPP']
lat = nc_file.variables['latitude']
lon = nc_file.variables['longitude']
time = nc_file.variables['time']

#print(nc_file.meta)
print(gdp_ppp)

                # # Open NCF
                # nc_file = xarray.open_dataset(ncf_path)
                # #print(nc_file)
                # max_v = nc_file.GDP_PPP.max()
                # min_v = nc_file.GDP_PPP.min()
                # print(max_v, 'MAX_V')
                # print(min_v, 'min_v')

                # scale_factor = (max_v - min_v) / ((2^32) - 1)
                # print(scale_factor)

                # # Write band 25(2015 data) out
                # nc_file.rio.write_crs('epgs:4326', inplace = True)
                # nc_file['GDP_PPP'][25].rio.to_raster('2015_gdp_extract_testing.tiff')

# # Extract Variable 
# gdp_ppp = nc_file['GDP_PPP']

# # Check CRS 
# #print(nc_file.rio.crs)

# # Check Scale factor 
# file_obj = nc.Dataset(ncf_path)
# print(file_obj.variables.keys())

# # Check min, max and n(number of bits for packed interger data type)

# min_val = file_obj.variables['GDP_PPP'].min
# print(min_val)

# add_offset = file_obj.variables['GDP_PPP'].add_offset
# scale_factor = file_obj.variables['GDP_PPP'].scale_factor
# print(scale_factor)
