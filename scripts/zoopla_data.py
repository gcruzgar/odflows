#!/usr/bin/env python3
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
import geopandas as gpd 
from utils import uk_plot

rentals = pd.read_csv("data/ZooplaRentals_Aggregate_NikLomax.txt", sep='\t')
sales = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t')    

#rentals.iloc[:,4:].sum()
#sales.iloc[:,4:].sum()  

sales_types = ['NumberOfMoves', 'MovesUnder250k', 'MovesOver250k', 
    'Terraced', 'Flat', 'SemiDetached', 'Detached',
    'Beds1to3', 'Beds4Plus']
rental_types = ['NumberOfRentals', 'RentUnder250', 'RentOver250',
    'Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow', 'PropertyTypeUnknown', 
    'Beds1to3', 'Beds4Plus']

sales_origin = pd.pivot_table(sales, values = sales_types, index = 'OriginWardName', aggfunc=np.sum) 
sales_destination = pd.pivot_table(sales, values = sales_types, index = 'DestinationWardName', aggfunc=np.sum)

rentals_origin = pd.pivot_table(rentals, values = rental_types, index = 'OriginWardName', aggfunc=np.sum) 
rentals_destination = pd.pivot_table(rentals, values = rental_types, index = 'DestinationWardName', aggfunc=np.sum)   

shp_path = "data/shapefiles/UK_Wards_2016.shp"
df = sales_origin
var_name = "NumberOfMoves"
title = "Number of moves originating from each ward"
uk_plot(shp_path, df, var_name, title)
