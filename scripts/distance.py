#!/usr/bin/env python3
import pandas as pd 
import geopandas as gpd 

sales = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t')            # data
map_df = gpd.read_file("data/shapefiles/GB_Wards_2015.shp")                         # shapefile

#merged = map_df.set_index("wd15nm").join(sales.set_index('OriginWardName')).dropna(subset=['NumberOfMoves'])  # data + shp

a = 'E05004153'
ai = map_df.loc[map_df['wd15cd']==a].index   # find index of first ward
ma = map_df['geometry'][ai.item()]           # find geometry of first ward
mac = ma.centroid                            # centre point of first ward

b = 'E05009501'
bi = map_df.loc[map_df['wd15cd']==b].index   # find index of second ward
mb = map_df['geometry'][bi.item()]           # find geometry of second ward
mbc = mb.centroid                            # centre point of second ward

ab_dist = ma.distance(mb)                    # distance between wards 
print(ab_dist)
