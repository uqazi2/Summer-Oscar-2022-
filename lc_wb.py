
from cProfile import label
import os
from turtle import color
import matplotlib.pyplot as plt
import configparser
import pandas as pd
import glob 
import seaborn as sns

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')

DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')

from misc import countries

def landchange_wb_inc(yeara, yearb, yearc, inc_group):  
    """
    Creates a plot of Land Cover type for given years and Income group
    """
    ############################################################################################# YEAR A

    # 2005 DATA 
    datapath_a = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yeara))
    dataread_a = pd.read_csv(datapath_a)
   
    # Convert to pandas dataframe
    data_a = pd.DataFrame(dataread_a)

    # Seperate Data by 'Low Mid Income'
    df_5_low_mid_a = data_a[data_a['World_Bank_Income'] == '{}'.format(inc_group)]

    #Get sums of Land Cover for Low income columns from YEAR A  
    a_evg_ndl_low = df_5_low_mid_a['Evergreen_Needleleaf'].sum()
    a_evg_brd_low = df_5_low_mid_a['Evergreen_Broadleaf'].sum()

    a_dec_ndl_low = df_5_low_mid_a['Decidous_Needleleaf'].sum()
    a_dec_brd_low = df_5_low_mid_a['Deciduous_Broadleaf'].sum()

    a_mix_for_low = df_5_low_mid_a['Mixed_Forest'].sum()

    a_cls_shr_low = df_5_low_mid_a['Closed_Shrubland'].sum()
    a_opn_shr_low = df_5_low_mid_a['Open_Shrubland'].sum()

    a_wdy_sav_low = df_5_low_mid_a['Woody_Savanas'].sum()
    a_sav_low = df_5_low_mid_a['Savanas'].sum()

    a_grs_low = df_5_low_mid_a['Grasslands'].sum()
    a_prm_wet_low = df_5_low_mid_a['Permanant_Wet_Lands'].sum()
    a_crp_low = df_5_low_mid_a['Croplands'].sum()
    a_urb_low = df_5_low_mid_a['Urban_and_Built_Up_Lands'].sum()
    a_nat_mos_low = df_5_low_mid_a['Croplands_or_Natural_Vegetation_Mosaics'].sum()
    a_sno_ice_low = df_5_low_mid_a['Permanant_Snow_and_Ice'].sum()
    a_brn_low = df_5_low_mid_a['Barren'].sum()
    a_wat_low = df_5_low_mid_a['Water'].sum()

    low_mid_lc_val_a = [a_evg_ndl_low, a_evg_brd_low, a_dec_ndl_low, a_dec_brd_low, a_mix_for_low, a_cls_shr_low, a_opn_shr_low, 
    a_wdy_sav_low, a_sav_low, a_grs_low, a_prm_wet_low, a_crp_low, a_urb_low, a_nat_mos_low, a_sno_ice_low, a_brn_low, a_wat_low]


    print(low_mid_lc_val_a, '{}'.format(inc_group), '{}'.format(yeara))


    ########################################################################################## YEAR B 

    # 2010 DATA 
    datapath_b = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearb))
    dataread_b = pd.read_csv(datapath_b)
   
    # Convert to pandas dataframe
    data_b = pd.DataFrame(dataread_b)

    # Seperate Data by 'Low Mid Income'
    df_low_mid_b = data_b[data_b['World_Bank_Income'] == '{}'.format(inc_group)]

    #Get sums of Land Cover for Low income columns from YEAR A  
    b_evg_ndl_low = df_low_mid_b['Evergreen_Needleleaf'].sum()
    b_evg_brd_low = df_low_mid_b['Evergreen_Broadleaf'].sum()

    b_dec_ndl_low = df_low_mid_b['Decidous_Needleleaf'].sum()
    b_dec_brd_low = df_low_mid_b['Deciduous_Broadleaf'].sum()

    b_mix_for_low = df_low_mid_b['Mixed_Forest'].sum()

    b_cls_shr_low = df_low_mid_b['Closed_Shrubland'].sum()
    b_opn_shr_low = df_low_mid_b['Open_Shrubland'].sum()

    b_wdy_sav_low = df_low_mid_b['Woody_Savanas'].sum()
    b_sav_low = df_low_mid_b['Savanas'].sum()

    b_grs_low = df_low_mid_b['Grasslands'].sum()
    b_prm_wet_low = df_low_mid_b['Permanant_Wet_Lands'].sum()
    b_crp_low = df_low_mid_b['Croplands'].sum()
    b_urb_low = df_low_mid_b['Urban_and_Built_Up_Lands'].sum()
    b_nat_mos_low = df_low_mid_b['Croplands_or_Natural_Vegetation_Mosaics'].sum()
    b_sno_ice_low = df_low_mid_b['Permanant_Snow_and_Ice'].sum()
    b_brn_low = df_low_mid_b['Barren'].sum()
    b_wat_low = df_low_mid_b['Water'].sum()

    low_mid_lc_val_b = [b_evg_ndl_low, b_evg_brd_low, b_dec_ndl_low, b_dec_brd_low, b_mix_for_low, b_cls_shr_low, b_opn_shr_low, 
    b_wdy_sav_low, b_sav_low, b_grs_low, b_prm_wet_low, b_crp_low, b_urb_low, b_nat_mos_low, b_sno_ice_low, b_brn_low, b_wat_low]

    print(low_mid_lc_val_b, '{}'.format(inc_group), '{}'.format(yearb))

    ########################################################################################## YEAR C

    # 2015 DATA 
    datapath_c = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearc))
    dataread_c = pd.read_csv(datapath_c)
   
    # Convert to pandas dataframe
    data_c = pd.DataFrame(dataread_c)

    # Seperate Data by 'Low Mid Income'
    df_low_mid_c = data_c[data_c['World_Bank_Income'] == '{}'.format(inc_group)]

    #Get sums of Land Cover for Low income columns from YEAR A  
    c_evg_ndl_low = df_low_mid_c['Evergreen_Needleleaf'].sum()
    c_evg_brd_low = df_low_mid_c['Evergreen_Broadleaf'].sum()

    c_dec_ndl_low = df_low_mid_c['Decidous_Needleleaf'].sum()
    c_dec_brd_low = df_low_mid_c['Deciduous_Broadleaf'].sum()

    c_mix_for_low = df_low_mid_c['Mixed_Forest'].sum()

    c_cls_shr_low = df_low_mid_c['Closed_Shrubland'].sum()
    c_opn_shr_low = df_low_mid_c['Open_Shrubland'].sum()

    c_wdy_sav_low = df_low_mid_c['Woody_Savanas'].sum()
    c_sav_low = df_low_mid_c['Savanas'].sum()

    c_grs_low = df_low_mid_c['Grasslands'].sum()
    c_prm_wet_low = df_low_mid_c['Permanant_Wet_Lands'].sum()
    c_crp_low = df_low_mid_c['Croplands'].sum()
    c_urb_low = df_low_mid_c['Urban_and_Built_Up_Lands'].sum()
    c_nat_mos_low = df_low_mid_c['Croplands_or_Natural_Vegetation_Mosaics'].sum()
    c_sno_ice_low = df_low_mid_c['Permanant_Snow_and_Ice'].sum()
    c_brn_low = df_low_mid_c['Barren'].sum()
    c_wat_low = df_low_mid_c['Water'].sum()

    low_mid_lc_val_c = [c_evg_ndl_low, c_evg_brd_low, c_dec_ndl_low, c_dec_brd_low, c_mix_for_low, c_cls_shr_low, c_opn_shr_low, 
    c_wdy_sav_low, c_sav_low, c_grs_low, c_prm_wet_low, c_crp_low, c_urb_low, c_nat_mos_low, c_sno_ice_low, c_brn_low, c_wat_low]

    print(low_mid_lc_val_c, '{}'.format(inc_group), '{}'.format(yearc))

    # Define Land Cover classes 
    land_cover = ['Evergreen Needleleaf', 'Evergreen Broadleaf', 'Deciduous Needleleaf', 'Deciduous Broadleaf', 'Mixed Forest',
                   'Closed Shrubland', 'Open Shrubland', 'Woody Savannas', 'Savanas', 'Grasslands', 'Permanent Wetlands', 'Croplands',
                   'Urban and Built up Areas', 'Croplands/Natural Vegetation Mosaics', 'Permanent Snow and Ice', 'Barren', 'Water']

    df = pd.DataFrame({'{}'.format(yeara):low_mid_lc_val_a, '{}'.format(yearb):low_mid_lc_val_b, '{}'.format(yearc):low_mid_lc_val_c}, index = land_cover)
    
    # Define Color Scheme 
    ax = df.plot.barh(color = ['violet','deepskyblue','navy'])

    # Set Background Color 
    ax.set_facecolor('ghostwhite')  
    ax.set

    # Set Title 
    plt.title('Land Cover Amounts by Time Period, for {} Countries'.format(inc_group), fontsize = 15, fontweight = 'bold')
    plt.xlabel('Area in Km2', fontsize = 11)

    # Add x, y gridlines
    ax.grid(b = True, color ='darkgrey',
        linestyle ='-', linewidth = 0.8,
        alpha = 0.2)

    # Re-orient Legend 
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [2,1,0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order])
    
    
    plt.show()


def landchange_wb_reg(yeara, yearb, yearc, reg_group):  
    """
    Creates a plot of Land Cover type for given years and Income group
    """
    ############################################################################################# YEAR A

    # 2005 DATA 
    datapath_a = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yeara))
    dataread_a = pd.read_csv(datapath_a)
   
    # Convert to pandas dataframe
    data_a = pd.DataFrame(dataread_a)

    # Seperate Data by Regional Group
    df_5_low_mid_a = data_a[data_a['World_Bank_Regions'] == '{}'.format(reg_group)]

    #Get sums of Land Cover for Low income columns from YEAR A  
    a_evg_ndl_low = df_5_low_mid_a['Evergreen_Needleleaf'].sum()
    a_evg_brd_low = df_5_low_mid_a['Evergreen_Broadleaf'].sum()

    a_dec_ndl_low = df_5_low_mid_a['Decidous_Needleleaf'].sum()
    a_dec_brd_low = df_5_low_mid_a['Deciduous_Broadleaf'].sum()

    a_mix_for_low = df_5_low_mid_a['Mixed_Forest'].sum()

    a_cls_shr_low = df_5_low_mid_a['Closed_Shrubland'].sum()
    a_opn_shr_low = df_5_low_mid_a['Open_Shrubland'].sum()

    a_wdy_sav_low = df_5_low_mid_a['Woody_Savanas'].sum()
    a_sav_low = df_5_low_mid_a['Savanas'].sum()

    a_grs_low = df_5_low_mid_a['Grasslands'].sum()
    a_prm_wet_low = df_5_low_mid_a['Permanant_Wet_Lands'].sum()
    a_crp_low = df_5_low_mid_a['Croplands'].sum()
    a_urb_low = df_5_low_mid_a['Urban_and_Built_Up_Lands'].sum()
    a_nat_mos_low = df_5_low_mid_a['Croplands_or_Natural_Vegetation_Mosaics'].sum()
    a_sno_ice_low = df_5_low_mid_a['Permanant_Snow_and_Ice'].sum()
    a_brn_low = df_5_low_mid_a['Barren'].sum()
    a_wat_low = df_5_low_mid_a['Water'].sum()

    low_mid_lc_val_a = [a_evg_ndl_low, a_evg_brd_low, a_dec_ndl_low, a_dec_brd_low, a_mix_for_low, a_cls_shr_low, a_opn_shr_low, 
    a_wdy_sav_low, a_sav_low, a_grs_low, a_prm_wet_low, a_crp_low, a_urb_low, a_nat_mos_low, a_sno_ice_low, a_brn_low, a_wat_low]


    print(low_mid_lc_val_a, '{}'.format(reg_group), '{}'.format(yeara))


    ########################################################################################## YEAR B 

    # 2010 DATA 
    datapath_b = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearb))
    dataread_b = pd.read_csv(datapath_b)
   
    # Convert to pandas dataframe
    data_b = pd.DataFrame(dataread_b)

    # Seperate Data by Regional group
    df_low_mid_b = data_b[data_b['World_Bank_Regions'] == '{}'.format(reg_group)]

    #Get sums of Land Cover for Low income columns from YEAR b  
    b_evg_ndl_low = df_low_mid_b['Evergreen_Needleleaf'].sum()
    b_evg_brd_low = df_low_mid_b['Evergreen_Broadleaf'].sum()

    b_dec_ndl_low = df_low_mid_b['Decidous_Needleleaf'].sum()
    b_dec_brd_low = df_low_mid_b['Deciduous_Broadleaf'].sum()

    b_mix_for_low = df_low_mid_b['Mixed_Forest'].sum()

    b_cls_shr_low = df_low_mid_b['Closed_Shrubland'].sum()
    b_opn_shr_low = df_low_mid_b['Open_Shrubland'].sum()

    b_wdy_sav_low = df_low_mid_b['Woody_Savanas'].sum()
    b_sav_low = df_low_mid_b['Savanas'].sum()

    b_grs_low = df_low_mid_b['Grasslands'].sum()
    b_prm_wet_low = df_low_mid_b['Permanant_Wet_Lands'].sum()
    b_crp_low = df_low_mid_b['Croplands'].sum()
    b_urb_low = df_low_mid_b['Urban_and_Built_Up_Lands'].sum()
    b_nat_mos_low = df_low_mid_b['Croplands_or_Natural_Vegetation_Mosaics'].sum()
    b_sno_ice_low = df_low_mid_b['Permanant_Snow_and_Ice'].sum()
    b_brn_low = df_low_mid_b['Barren'].sum()
    b_wat_low = df_low_mid_b['Water'].sum()

    low_mid_lc_val_b = [b_evg_ndl_low, b_evg_brd_low, b_dec_ndl_low, b_dec_brd_low, b_mix_for_low, b_cls_shr_low, b_opn_shr_low, 
    b_wdy_sav_low, b_sav_low, b_grs_low, b_prm_wet_low, b_crp_low, b_urb_low, b_nat_mos_low, b_sno_ice_low, b_brn_low, b_wat_low]

    print(low_mid_lc_val_b, '{}'.format(reg_group), '{}'.format(yearb))

    ########################################################################################## YEAR C

    # 2015 DATA 
    datapath_c = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearc))
    dataread_c = pd.read_csv(datapath_c)
   
    # Convert to pandas dataframe
    data_c = pd.DataFrame(dataread_c)

    # Seperate Data by World Bank Regions 
    df_low_mid_c = data_c[data_c['World_Bank_Regions'] == '{}'.format(reg_group)]

    #Get sums of Land Cover for Low income columns from YEAR c  
    c_evg_ndl_low = df_low_mid_c['Evergreen_Needleleaf'].sum()
    c_evg_brd_low = df_low_mid_c['Evergreen_Broadleaf'].sum()

    c_dec_ndl_low = df_low_mid_c['Decidous_Needleleaf'].sum()
    c_dec_brd_low = df_low_mid_c['Deciduous_Broadleaf'].sum()

    c_mix_for_low = df_low_mid_c['Mixed_Forest'].sum()

    c_cls_shr_low = df_low_mid_c['Closed_Shrubland'].sum()
    c_opn_shr_low = df_low_mid_c['Open_Shrubland'].sum()

    c_wdy_sav_low = df_low_mid_c['Woody_Savanas'].sum()
    c_sav_low = df_low_mid_c['Savanas'].sum()

    c_grs_low = df_low_mid_c['Grasslands'].sum()
    c_prm_wet_low = df_low_mid_c['Permanant_Wet_Lands'].sum()
    c_crp_low = df_low_mid_c['Croplands'].sum()
    c_urb_low = df_low_mid_c['Urban_and_Built_Up_Lands'].sum()
    c_nat_mos_low = df_low_mid_c['Croplands_or_Natural_Vegetation_Mosaics'].sum()
    c_sno_ice_low = df_low_mid_c['Permanant_Snow_and_Ice'].sum()
    c_brn_low = df_low_mid_c['Barren'].sum()
    c_wat_low = df_low_mid_c['Water'].sum()

    low_mid_lc_val_c = [c_evg_ndl_low, c_evg_brd_low, c_dec_ndl_low, c_dec_brd_low, c_mix_for_low, c_cls_shr_low, c_opn_shr_low, 
    c_wdy_sav_low, c_sav_low, c_grs_low, c_prm_wet_low, c_crp_low, c_urb_low, c_nat_mos_low, c_sno_ice_low, c_brn_low, c_wat_low]

    print(low_mid_lc_val_c, '{}'.format(reg_group), '{}'.format(yearc))

    # Define Land Cover classes 
    land_cover = ['Evergreen Needleleaf', 'Evergreen Broadleaf', 'Deciduous Needleleaf', 'Deciduous Broadleaf', 'Mixed Forest',
                   'Closed Shrubland', 'Open Shrubland', 'Woody Savannas', 'Savanas', 'Grasslands', 'Permanent Wetlands', 'Croplands',
                   'Urban and Built up Areas', 'Croplands/Natural Vegetation Mosaics', 'Permanent Snow and Ice', 'Barren', 'Water']

    df = pd.DataFrame({'{}'.format(yeara):low_mid_lc_val_a, '{}'.format(yearb):low_mid_lc_val_b, '{}'.format(yearc):low_mid_lc_val_c}, index = land_cover)
    
    # Define Color Scheme 
    ax = df.plot.barh(color = ['violet','deepskyblue','navy'])

    # Set Background Color 
    ax.set_facecolor('ghostwhite')  
    ax.set

    # Set Title 
    plt.title('Land Cover Amounts by Time Period, for {}'.format(reg_group), fontsize = 15, fontweight = 'bold')
    plt.xlabel('Area in Km2', fontsize = 11)

    # Add x, y gridlines
    ax.grid(b = True, color ='darkgrey',
        linestyle ='-', linewidth = 0.8,
        alpha = 0.2)

    # Re-orient Legend 
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [2,1,0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order])
    
    
    plt.show()


def gdp_ppp_tot_reg(yeara, yearb, yearc):

    # 2005 DATA 
    datapath_a = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yeara))
    dataread_a = pd.read_csv(datapath_a)

    # Sort Data by World Bank Income groups 
    mean_gdp_a = dataread_a.groupby(['World_Bank_Regions'])['gdp_mean'].mean()

    # 2010 DATA 
    datapath_b = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearb))
    dataread_b = pd.read_csv(datapath_b)

    # Sort Data by World Bank Income groups 
    mean_gdp_b = dataread_b.groupby(['World_Bank_Regions'])['gdp_mean'].mean()

    # 2015 DATA 
    datapath_c = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearc))
    dataread_c = pd.read_csv(datapath_c)

    # Sort Data by World Bank Income groups 
    mean_gdp_c = dataread_c.groupby(['World_Bank_Regions'])['gdp_mean'].mean()

    # Define Income Groups for Plotting 
    region_groups = ['Advanced Economies','Caucasus and Central Asia', 'Emerging and Developing Asia', 'Emerging and Developing Europe',  'Latin America and the Caribbean', 
        'Middle East, North Africa, Afghanistan, and Pakistan', 'Sub-Sahara Africa']

    df = pd.DataFrame({'{}'.format(yeara):mean_gdp_a, '{}'.format(yearb):mean_gdp_b, '{}'.format(yearc):mean_gdp_c}, index = region_groups)
    print(df)
    print(df.columns)

    # fig, (ax1,ax2,ax3) = plt.subplots(3)

    # ax1.barh(region_groups,mean_gdp_a)

    # ax2.barh(region_groups,mean_gdp_b)

    # ax3.barh(region_groups,mean_gdp_c)

    ax = df.plot.barh(color = ['violet','deepskyblue','navy'])
    plt.title('Mean GDP PPP, by World Bank Regions')

    
    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width(), i.get_y(),
             str(round((i.get_width()), 2)),
             fontsize = 10, 
             fontweight ='normal',
             color ='darkgrey')

    
    #Re-orient Legend 
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [2,1,0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order])
    
    # Set Background Color 
    ax.set_facecolor('ghostwhite')  
    ax.set

    # Set Title 
    plt.xlabel('Reported in 2011 USD', fontsize = 11)

    # Add x, y gridlines
    ax.grid(b = True, color ='darkgrey',
        linestyle ='-', linewidth = 0.8,
        alpha = 0.2)

    plt.show()


def gdp_ppp_tot_inc_mean(yeara, yearb, yearc):

    # 2005 DATA 
    datapath_a = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yeara))
    dataread_a = pd.read_csv(datapath_a)

    # Sort Data by World Bank Income groups 
    mean_gdp_a = dataread_a.groupby(['World_Bank_Income'])['gdp_mean'].mean()
    
    # 2010 DATA 
    datapath_b = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearb))
    dataread_b = pd.read_csv(datapath_b)

    # Sort Data by World Bank Income groups 
    mean_gdp_b = dataread_b.groupby(['World_Bank_Income'])['gdp_mean'].mean()

    # 2015 DATA 
    datapath_c = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearc))
    dataread_c = pd.read_csv(datapath_c)

    # Sort Data by World Bank Income groups 
    mean_gdp_c = dataread_c.groupby(['World_Bank_Income'])['gdp_mean'].mean()
    
    # Define Income Groups for Plotting 
    income_groups = ['Low Income', 'Lower Middle Income', 'Upper Middle Income', 'High Income']

    df = pd.DataFrame({'{}'.format(yeara):mean_gdp_a, '{}'.format(yearb):mean_gdp_b, '{}'.format(yearc):mean_gdp_c}, index = income_groups)
    print(df)
    print(df.columns)

    # fig, (ax1,ax2,ax3) = plt.subplots(3)

    # ax1.barh(region_groups,mean_gdp_a)

    # ax2.barh(region_groups,mean_gdp_b)

    # ax3.barh(region_groups,mean_gdp_c)

    ax = df.plot.barh(color = ['violet','deepskyblue','navy'])
    #ax = df.plot.barh(color = ['mediumorchid','steelblue','mediumturquoise'])
    plt.title('Mean GDP PPP, by World Bank Regions')

    
    # # Add annotation to bars
    # for i in ax.patches:
    #     plt.text(i.get_width(), i.get_y(),
    #          str(round((i.get_width()), 2)),
    #          fontsize = 10, 
    #          fontweight ='normal',
    #          color ='darkgrey')

    
    #Re-orient Legend 
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [2,1,0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order])
    
    # Set Background Color 
    ax.set_facecolor('ghostwhite')  
    ax.set

    # Set Title 
    plt.xlabel('Reported in 2011 USD', fontsize = 11)

    # Add x, y gridlines
    ax.grid(b = True, color ='darkgrey',
        linestyle ='-', linewidth = 0.8,
        alpha = 0.2)

    plt.show()


def population_growth_wbi(yeara, yearb, yearc):
    """
    Creates chart of population data by world bank groups 
    """  
    
    # 2005 DATA 
    datapath_a = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yeara))
    dataread_a = pd.read_csv(datapath_a)
   
    # 2010 DATA 
    datapath_b = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearb))
    dataread_b = pd.read_csv(datapath_b)

    # 2015 DATA 
    datapath_c = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearc))
    dataread_c = pd.read_csv(datapath_c)

    
    # Convert to pandas dataframe
    data_a = pd.DataFrame(dataread_a)
    data_b = pd.DataFrame(dataread_b)
    data_c = pd.DataFrame(dataread_c)

    # Get Population data for each year 
    pop_a = data_a.groupby(['World_Bank_Income'])['Population'].sum()
    pop_b = data_b.groupby(['World_Bank_Income'])['Population'].sum()
    pop_c = data_c.groupby(['World_Bank_Income'])['Population'].sum()

    x = ['Low Income', 'Lower Middle Income', 'Upper Middle Income', 'High Income']

    df = pd.DataFrame({'{}'.format(yeara):pop_a, '{}'.format(yearb):pop_b, '{}'.format(yearc):pop_c}, index = x)
    #df = pd.DataFrame({'{}'.format(yearc):pop_c, '{}'.format(yearb):pop_b,  '{}'.format(yeara):pop_a,}, index = x)
    ax = df.plot.barh(color = ['mediumorchid','steelblue','mediumturquoise'])

    plt.title('Population by World Bank Income Group', fontsize = 15, fontweight = 'bold')

    # Add annotation to bar
    # for i in ax.patches:
    #     plt.text(i.get_width()+0.2, i.get_y()+0.5,
    #          str(round((i.get_width()), 2)),
    #          fontsize = 6, fontweight ='bold', ha = 'center', va = 'center',
    #          color ='grey')

    

    plt.xlabel('Population in Millions', fontsize = 11)

    handles, labels = plt.gca().get_legend_handles_labels()
    order = [2,1,0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order])

    # Add x, y gridlines
    ax.grid(b = True, color ='darkgrey',
        linestyle ='-.', linewidth = 0.8,
        alpha = 0.2)
    print(df)

    plt.show()


def population_growth_wbr(yeara, yearb, yearc):
    """
    Creates chart of population data by world bank groups 
    """  
    
    # 2005 DATA 
    datapath_a = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yeara))
    dataread_a = pd.read_csv(datapath_a)
   
    # 2010 DATA 
    datapath_b = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearb))
    dataread_b = pd.read_csv(datapath_b)

    # 2015 DATA 
    datapath_c = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearc))
    dataread_c = pd.read_csv(datapath_c)

    
    # Convert to pandas dataframe
    data_a = pd.DataFrame(dataread_a)
    data_b = pd.DataFrame(dataread_b)
    data_c = pd.DataFrame(dataread_c)

    # Get Population data for each year 
    pop_a = data_a.groupby(['World_Bank_Regions'])['Population'].sum()
    pop_b = data_b.groupby(['World_Bank_Regions'])['Population'].sum()
    pop_c = data_c.groupby(['World_Bank_Regions'])['Population'].sum()

    x = ['Advanced Economies','Caucasus and Central Asia', 'Emerging and Developing Asia', 'Emerging and Developing Europe',  'Latin America and the Caribbean', 
        'Middle East, North Africa, Afghanistan, and Pakistan', 'Sub-Sahara Africa']

    df = pd.DataFrame({'{}'.format(yeara):pop_a, '{}'.format(yearb):pop_b, '{}'.format(yearc):pop_c}, index = x)
    #df = pd.DataFrame({'{}'.format(yearc):pop_c, '{}'.format(yearb):pop_b,  '{}'.format(yeara):pop_a,}, index = x)
    ax = df.plot.barh(color = ['violet','deepskyblue','navy'])

    plt.title('Population by World Bank Regional Group', fontsize = 15, fontweight = 'bold')

    # Add annotation to bar
    # for i in ax.patches:
    #     plt.text(i.get_width()+0.2, i.get_y()+0.5,
    #          str(round((i.get_width()), 2)),
    #          fontsize = 6, fontweight ='bold', ha = 'center', va = 'center',
    #          color ='grey')

    

    plt.xlabel('Population in Millions', fontsize = 11)

    handles, labels = plt.gca().get_legend_handles_labels()
    order = [2,1,0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order])

    # Add x, y gridlines
    ax.grid(b = True, color ='darkgrey',
        linestyle ='-.', linewidth = 0.8,
        alpha = 0.2)
    print(df)

    plt.show()
inc_group = 'Low Income'

yeara = 2005
yearb = 2010
yearc = 2015
reg_group = 'Sub-Sahara Africa'
#landchange_wb_inc(yeara, yearb, yearc, inc_group)
#landchange_wb_reg(yeara,yearb,yearc,reg_group)
#gdp_ppp_tot_reg(yeara,yearb,yearc)
#gdp_ppp_tot_inc_mean(yeara,yearb,yearc)
#population_growth_wbi(yeara,yearb,yearc)
population_growth_wbr(yeara,yearb,yearc)


def gdp_ppp_mean_reg(yeara, yearb, yearc): ############################

    # 2005 DATA 
    datapath_a = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yeara))
    dataread_a = pd.read_csv(datapath_a)

    # Sort Data by World Bank Income groups 
    mean_gdp_a = dataread_a.groupby(['World_Bank_Regions'])['gdp_sum'].mean()

    # 2010 DATA 
    datapath_b = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearb))
    dataread_b = pd.read_csv(datapath_b)

    # Sort Data by World Bank Income groups 
    mean_gdp_b = dataread_b.groupby(['World_Bank_Regions'])['gdp_sum'].mean()

    # 2015 DATA 
    datapath_c = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearc))
    dataread_c = pd.read_csv(datapath_c)

    # Sort Data by World Bank Income groups 
    mean_gdp_c = dataread_c.groupby(['World_Bank_Regions'])['gdp_sum'].mean()

    # Define Income Groups for Plotting 
    region_groups = ['Caucasus and Central Asia', 'Emerging and Developing Europe', 'Emerging and Developing Asia', 'Advanced Economies', 'Latin America and the Caribbean', 
        'Sub-Sahara Africa', 'Middle East, North Africa, Afghanistan, and Pakistan']

    df = pd.DataFrame({'{}'.format(yeara):mean_gdp_a, '{}'.format(yearb):mean_gdp_b, '{}'.format(yearc):mean_gdp_c}, index = region_groups)
    print(df)
    print(df.columns)

    # fig, (ax1,ax2,ax3) = plt.subplots(3)

    # ax1.barh(region_groups,mean_gdp_a)

    # ax2.barh(region_groups,mean_gdp_b)

    # ax3.barh(region_groups,mean_gdp_c)

    ax = df.plot.barh(color = ['violet','deepskyblue','navy'])
    plt.title('Mean GDP PPP, by World Bank Regions')

    
    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width(), i.get_y(),
             str(round((i.get_width()), 2)),
             fontsize = 10, 
             fontweight ='normal',
             color ='darkgrey')

    
    #Re-orient Legend 
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [2,1,0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order])
    
    # Set Background Color 
    ax.set_facecolor('ghostwhite')  
    ax.set

    # Set Title 
    plt.xlabel('Reported in 2011 USD', fontsize = 11)

    # Add x, y gridlines
    ax.grid(b = True, color ='darkgrey',
        linestyle ='-', linewidth = 0.8,
        alpha = 0.2)

    plt.show()

def gdp_ppp_wb_reg(yeara, yearb, yearc, reg_group): ###################

    # 2005 DATA 
    datapath_a = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yeara))
    dataread_a = pd.read_csv(datapath_a)
   
    # Convert to pandas dataframe
    data_a = pd.DataFrame(dataread_a)

    # Seperate Data by Regional Group
    gdp_ppp_a = data_a[data_a['World_Bank_Regions'] == '{}'.format(reg_group)]

    # Get sum of mean amounts 
    gdp_a = gdp_ppp_a['gdp_mean'].mean()
    print(gdp_a)
    
    mean_gdp = dataread_a.groupby(['World_Bank_Income'])['gdp_sum'].mean()
    
    # 2010 DATA 
    datapath_b = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearb))
    dataread_b = pd.read_csv(datapath_b)
   
    # Convert to pandas dataframe
    data_b = pd.DataFrame(dataread_b)

    # Seperate Data by Regional Group
    gdp_ppp_b = data_b[data_b['World_Bank_Regions'] == '{}'.format(reg_group)]

    # Get sum of mean amounts 
    gdp_b = gdp_ppp_b['gdp_mean'].mean()
    print(gdp_b)

    # 2015 DATA 
    datapath_c = os.path.join(DATA_INTERMEDIATE, 'TOTAL_STATS', 'merged', 'merged-{}-data.csv'.format(yearc))
    dataread_c = pd.read_csv(datapath_c)
   
    # Convert to pandas dataframe
    data_c = pd.DataFrame(dataread_c)

    # Seperate Data by Regional Group
    gdp_ppp_c = data_c[data_c['World_Bank_Regions'] == '{}'.format(reg_group)]

    # Get sum of mean amounts 
    gdp_c = gdp_ppp_c['gdp_mean'].mean()
    print(gdp_c)

    # Define Income Groups for Plotting 
    region_groups = ['Caucasus and Central Asia', 'Emerging and Developing Europe', 'Emerging and Developing Asia', 'Advanced Economies', 'Latin America and the Caribbean', 
        'Sub-Sahara Africa', 'Middle East, North Africa, Afghanistan, and Pakistan']

    # Append to Dataframe for graphing 
    df = pd.DataFrame({'{}'.format(yeara):gdp_a, '{}'.format(yearb):gdp_b, '{}'.format(yearc):gdp_c}, index = region_groups)

    # Define Color Scheme 
    ax = df.plot.barh(color = ['violet','deepskyblue','navy'])

    # Set Background Color 
    ax.set_facecolor('ghostwhite')  
    ax.set

    # Set Title 
    plt.title('Mean GDP by World Bank Regions',  fontsize = 15, fontweight = 'bold')
    plt.xlabel('Reported in 2011 USD, Billions', fontsize = 11)

    # Add x, y gridlines
    ax.grid(b = True, color ='darkgrey',
        linestyle ='-', linewidth = 0.8,
        alpha = 0.2)

    # Re-orient Legend 
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [2,1,0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order])
    
    
    plt.show()




