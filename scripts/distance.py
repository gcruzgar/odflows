#!/usr/bin/env python3
import pandas as pd 
import geopandas as gpd 

sales = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t').dropna()            # data
map_df = gpd.read_file("data/shapefiles/UK_Wards_2016.shp")                         # shapefile

#merged = map_df.set_index("wd15nm").join(sales.set_index('OriginWardName')).dropna(subset=['NumberOfMoves'])  # data + shp

dist_list = []
for i in sales.index:

    a = sales['OriginWardCode'][i]               # ward code
    ai = map_df.loc[map_df['wd16cd']==a].index   # find index of first ward
    ma = map_df['geometry'][ai.item()]           # find geometry of first ward
    mac = ma.centroid                            # centre point of first ward

    b = sales['DestinationWardCode'][i]          # ward code
    bi = map_df.loc[map_df['wd16cd']==b].index   # find index of second ward
    mb = map_df['geometry'][bi.item()]           # find geometry of second ward       
    mbc = mb.centroid                            # centre point of second ward

    ab = mac.distance(mbc)                       # distance between centroids
    dist_list.append(ab)             

sales['distance'] = dist_list
