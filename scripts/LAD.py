#!/usr/bin/env python3
import argparse
import numpy as np 
import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
from utils import uk_plot, categ, categ_plot

def main():

    if args.r:
        rs = 'rentals'
        print("Loading rental data...")
        df = pd.read_csv("data/ZooplaRentals_Aggregate_NikLomax.txt", sep='\t')
        df.rename(index=str, columns={'NumberOfRentals': 'Total'}, inplace=True)
        df_types = ['Total', 'RentUnder250', 'RentOver250',
            'Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow', 'PropertyTypeUnknown', 
            'Beds1to3', 'Beds4Plus']
    else:
        rs = 'sales'
        print("Loading sales data...")
        df = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t')
        df.rename(index=str, columns={'NumberOfMoves': 'Total'}, inplace=True)   
        df_types = ['Total', 'MovesUnder250k', 'MovesOver250k', 
            'Terraced', 'Flat', 'SemiDetached', 'Detached',
            'Beds1to3', 'Beds4Plus']

    df_origin = pd.pivot_table(df, values = df_types, index = 'OriginWardCode', aggfunc=np.sum)    
    df_destination = pd.pivot_table(df, values = df_types, index = 'DestinationWardCode', aggfunc=np.sum)   

    shp_path = "data/shapefiles/GB_Wards_2016.shp"
    geo_code = 'wd16cd'

    map_df = gpd.read_file(shp_path) 
    merged = map_df.merge(df_origin, left_on=geo_code, right_on=df_origin.index, how='left')
    #merged=merged.loc[~merged[geo_code].str.startswith('S', na=False)] # drop Scottish wards

    # aggregate to LADs
    lad_map = pd.pivot_table(merged, values=df_types, index='lad16cd', aggfunc=np.sum)

    # lad category plot
    cat = args.c[0]
    cat_df = categ(lad_map, cat, args.r)
    categ_plot("data/shapefiles/GB_LAD_2016.shp", 'lad16cd', cat_df, cat, ('Most frequent %s - %s' %  (rs, cat)))
    plt.show()

    # filter by LAD
    lad = 'E08000035' # LAD code, can also use lad16nm for name
    lad_df = merged.loc[merged['lad16cd']==lad]

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    parser.add_argument("-c", type=str, nargs=1, default=['dwelling'], 
        help="Category to plot: 'beds', 'dwelling', 'price' or 'RUC11'.")
    args = parser.parse_args()
    main()