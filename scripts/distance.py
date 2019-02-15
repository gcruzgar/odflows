#!/usr/bin/env python3
import pandas as pd 
import geopandas as gpd 

sales = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t')            # data
map_df = gpd.read_file("data/shapefiles/GB_Wards_2015.shp")                         # shapefile

#merged = map_df.set_index("wd15nm").join(sales.set_index('OriginWardName')).dropna(subset=['NumberOfMoves'])  # data + shp

a = 'E05001526'
ag = map_df.loc[map_df['wd15cd']==a, 'geometry'] # find geometry of first ward
a_cen = ag.centroid                              # centre point of ward

b = 'E05000026'
bg = map_df.loc[map_df['wd15cd']==b, 'geometry'] # find geometry of second ward
b_cen = bg.centroid                              # centre point of ward

#ab_dist = ag.distance(bg)                        # distance between wards (not working?)
