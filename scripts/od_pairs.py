#!/usr/bin/env python3
import argparse
import numpy as np 
import pandas as pd 
import geopandas as gpd 
from utils import uk_plot, top_10
import matplotlib.pyplot as plt 

sales = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t').dropna(axis=0, how='any')

sales_types = ['NumberOfMoves', 'MovesUnder250k', 'MovesOver250k', 
    'Terraced', 'Flat', 'SemiDetached', 'Detached',
    'Beds1to3', 'Beds4Plus']

sales_origin = pd.pivot_table(sales, values = sales_types, index = 'OriginWardName', aggfunc=np.sum)
sales_destination = pd.pivot_table(sales, values = sales_types, index = 'DestinationWardName', aggfunc=np.sum)
sales_net = sales_destination - sales_origin

shp_path = "data/shapefiles/UK_Wards_2016.shp"
var_name = 'NumberOfMoves'
uk_plot(shp_path, sales_net, var_name, 'sales - '+var_name)
top_10(sales_net,var_name, var_name+' (net) - Top 10')
plt.show()
