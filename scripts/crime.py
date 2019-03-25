#!/usr/bin/env python3
import argparse
import numpy as np 
import pandas as pd 
from os import listdir
import geopandas as gpd 
import matplotlib.pyplot as plt 
from utils import uk_plot, Ward_to_LAD

def main():

    crime_type = args.c[0] 

    LSOA_Ward = pd.read_csv("data/EW_LSOA_Ward_Lookup_2016.csv") # LSOA to Ward lookup

    data_path = "data/crime/"
    folder_list = listdir(data_path)

    crime = pd.DataFrame()
    for folder_name in sorted(folder_list):

        file_list = listdir(data_path+folder_name)

        print("Loading %s data..." % folder_name)
        for file_name in file_list:

            f_crime = pd.read_csv(data_path+folder_name+r'/'+file_name) #load crime data for sepcific file 

            f_crime = f_crime[['LSOA code', 'Crime type']] # only interested in crime type and location
            f_crime = f_crime.loc[f_crime['Crime type'] == crime_type ] # filter by crime type

            crime = pd.concat([crime, f_crime], axis=0) # join data from all files

    crime_rate = pd.DataFrame(crime['LSOA code'].value_counts()).rename(index=str, columns={'LSOA code': 'Crime rate'}) # number of crimes per LSOA
    crime_conv = crime_rate.merge(LSOA_Ward, left_on=crime_rate.index, right_on='LSOA11CD', how='right')

    crime_ward = pd.pivot_table(crime_conv, values=['Crime rate'], index='WD16CD', aggfunc=np.sum) # number of crimes per ward

    if args.lad:
        oa='LAD'
        lad_map = Ward_to_LAD(crime_ward, df_types=['Crime rate']) # aggregate to Local Authority District
        shp_path = "data/shapefiles/GB_LAD_2016.shp"
        geo_code = 'lad16cd'
        uk_plot(shp_path, geo_code, lad_map, 'Crime rate', title=('average crime rate - %s' % crime_type), cmap='OrRd') # plot crime data
    else:
        oa='ward'
        shp_path = "data/shapefiles/GB_Wards_2016.shp"
        geo_code = 'wd16cd'
        uk_plot(shp_path, geo_code, crime_ward, 'Crime rate', title=('average crime rate - %s' % crime_type), cmap='OrRd') # plot crime data

    plt.show()

    if args.s:
        print("Saving outputs...")
        crime_ward.to_csv("data/"+crime_type+"_"+oa+"_2016.csv")

if __name__ == "__main__":
        
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", action='store_true',
        help="save outputs to csv.")
    parser.add_argument("-c", type=str, nargs=1, default=["Burglary"], 
        help="Category to plot: 'beds', 'dwelling' or 'price'.")
    parser.add_argument("-lad", action='store_true', 
        help="aggregate to LAD.")
    args = parser.parse_args()

    main()
