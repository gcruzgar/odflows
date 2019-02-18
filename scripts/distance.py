#!/usr/bin/env python3
import pandas as pd 
import geopandas as gpd 

sales = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t').dropna()     # sales 
rentals = pd.read_csv("data/ZooplaRentals_Aggregate_NikLomax.txt", sep='\t').dropna() # rentals        
map_df = gpd.read_file("data/shapefiles/UK_Wards_2016.shp")                           # shapefile

def ward_distance(df, map_df):

    print("Calculating distances...")

    dist_list = []
    for i in df.index:

        a = df['OriginWardCode'][i]                 # ward code
        ai = map_df.loc[map_df['wd16cd']==a].index  # find index of first ward
        ma = map_df['geometry'][ai.item()]          # find geometry of first ward
        mac = ma.centroid                           # centre point of first ward

        b = df['DestinationWardCode'][i]            # ward code
        bi = map_df.loc[map_df['wd16cd']==b].index  # find index of second ward
        mb = map_df['geometry'][bi.item()]          # find geometry of second ward       
        mbc = mb.centroid                           # centre point of second ward

        ab = mac.distance(mbc)                      # distance between centroids
        dist_list.append(ab)             

    df['distance'] = dist_list
    #df.to_csv("data/rentals_and_distance.csv")

ward_distance(rentals, map_df)
