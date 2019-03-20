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

    # if args.f == 'net':
    #     df = df.dropna(subset=['DestinationWardCode'])
        
    df_dict = {
        'df_origin': pd.pivot_table(df, values = df_types, index = 'OriginWardCode', aggfunc=np.sum),
        'df_destination': pd.pivot_table(df, values = df_types, index = 'DestinationWardCode', aggfunc=np.sum),
    }
    df_dict['df_net'] = df_dict['df_destination'] - df_dict['df_origin']


    df_target = df_dict['df_origin']    

    map_df = gpd.read_file("data/shapefiles/GB_Wards_2016.shp") 
    merged = map_df.merge(df_target, left_on='wd16cd', right_on=df_target.index, how='left')
    merged=merged.loc[~merged['wd16cd'].str.startswith('S', na=False)] # drop Scottish wards

    # aggregate to LADs
    lad_map = pd.pivot_table(merged, values=df_types, index='lad16cd', aggfunc=np.sum)

    shp_path = "data/shapefiles/GB_LAD_2016.shp"
    geo_code = 'lad16cd'

    # plots
    var_name = args.var_name
    uk_plot(shp_path, geo_code, lad_map, var_name, 'in-flow - %s' % (var_name))

    # lad category plot
    cat = args.c[0]
    cat_df = categ(lad_map, cat, args.r)
    categ_plot(shp_path, geo_code, cat_df, cat, ('Most frequent %s - %s' %  (rs, cat)))

    plt.show()

    # filter by LAD
    lad = 'E08000035' # LAD code, can also use lad16nm for name
    lad_df = merged.loc[merged['lad16cd']==lad]

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default="Total",
        help="Variable to plot, e.g. 'Total' or 'Beds1to3'.")
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    parser.add_argument("-c", type=str, nargs=1, default=['dwelling'], 
        help="Category to plot: 'beds', 'dwelling', 'price' or 'RUC11'.")
    args = parser.parse_args()
    main()