#!/usr/bin/env python3
import numpy as np 
import pandas as pd 
from os import listdir
import geopandas as gpd 
import matplotlib.pyplot as plt 
from utils import uk_plot

data_path = "data/crime/2016-04/"
file_list = listdir(data_path)

LSOA_Ward = pd.read_csv("data/EW_LSOA_Ward_Lookup_2016.csv") # LSOA to Ward lookup

crime = pd.DataFrame()
for file_name in file_list:

    f_crime = pd.read_csv(data_path+file_name) #load crime data for sepcific file 

    f_crime = f_crime[['LSOA code', 'Crime type']] # only interested in crime type and location
    f_crime = f_crime.loc[f_crime['Crime type'] == 'Burglary'] # filter by crime type

    crime = pd.concat([crime, f_crime], axis=0) # join data from all files

print(crime.head())
crime_rate = pd.DataFrame(crime['LSOA code'].value_counts()).rename(index=str, columns={'LSOA code': 'Crime rate'}) # number of crimes per LSOA
crime_conv = crime_rate.merge(LSOA_Ward, left_on=crime_rate.index, right_on='LSOA11CD', how='right').fillna(value=0)

crime_ward = pd.pivot_table(crime_conv, values=['Crime rate'], index='WD16CD', aggfunc=np.sum)

shp_path = "data/shapefiles/GB_Wards_2016.shp"
geo_code = 'wd16cd'

uk_plot(shp_path, geo_code, crime_ward,'Crime rate', 'average crime rate - burglary', cmap='OrRd')
plt.show()
