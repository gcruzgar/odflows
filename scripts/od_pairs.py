#!/usr/bin/env python3
import argparse
import numpy as np 
import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
from utils import uk_plot, top_10, categ_plot

def categ(df, cat, r=False):

    if r == False:
        cat_types = {
            'beds': ['Beds1to3', 'Beds4Plus'], 
            'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached'], 
            'price': ['MovesUnder250k', 'MovesOver250k']
        }
    else:
        cat_types = {
            'beds': ['Beds1to3', 'Beds4Plus'], 
            'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow'], 
            'price': ['RentUnder250', 'RentOver250']
        }

    # most common type in each ward
    df[cat] = df[cat_types[cat]].idxmax(axis=1)

    return df

def main():

    var_name = args.var_name
    
    if args.r:
        r=True
        print("Loading rental data...")
        df = pd.read_csv("data/ZooplaRentals_Aggregate_NikLomax.txt", sep='\t').dropna(subset=['DestinationWardCode'])
        df.rename(index=str, columns={'NumberOfRentals': 'Total'}, inplace=True)
        df_types = ['Total', 'RentUnder250', 'RentOver250',
            'Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow', 'PropertyTypeUnknown', 
            'Beds1to3', 'Beds4Plus']
    else:
        r=False
        print("Loading sales data...")
        df = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t').dropna(subset=['DestinationWardCode'])
        df.rename(index=str, columns={'NumberOfMoves': 'Total'}, inplace=True)   
        df_types = ['Total', 'MovesUnder250k', 'MovesOver250k', 
            'Terraced', 'Flat', 'SemiDetached', 'Detached',
            'Beds1to3', 'Beds4Plus']

    # Note: dropna is used to only keep available od pairs

    df_dict = {
        'df_origin': pd.pivot_table(df, values = df_types, index = 'OriginWardName', aggfunc=np.sum),
        'df_destination': pd.pivot_table(df, values = df_types, index = 'DestinationWardName', aggfunc=np.sum),
    }
    df_dict['df_net'] = df_dict['df_destination'] - df_dict['df_origin']

    print("\nMoves from origin: \n{}".format(df_dict['df_origin'].sum()))
    print("\nMoves to destination: \n{}".format(df_dict['df_destination'].sum()))

    shp_path = "data/shapefiles/GB_Wards_2015.shp"

    # raw - net
    uk_plot(shp_path, df_dict['df_net'], var_name, 'net df - '+var_name)
    #top_10(df_net,var_name, var_name+' (net) - Top 10')

    # normalised
    if var_name != 'Total':
        pc_df_origin =  df_dict['df_origin'].drop(columns=['Total']).div(df_dict['df_origin']['Total'], axis=0)
        pc_df_destination = df_dict['df_destination'].drop(columns=['Total']).div(df_dict['df_destination']['Total'], axis=0)
        pc_df_net = pc_df_destination - pc_df_origin

        uk_plot(shp_path, pc_df_net, var_name, 'df - '+var_name+' - net normalised')
        #top_10(pc_df_net,var_name, var_name+' (net normalised) - Top 10')
            
    # categorical
    if args.c:

        cat = args.c[0]
        cat_df = categ(df_dict['df_origin'], cat, r)
        categ_plot(shp_path, cat_df, cat, 'Most frequent - '+cat)

    plt.show()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default="Total",
        help="Variable to plot, e.g. 'Total' or 'Beds1to3'.")
    parser.add_argument("-c", type=str, nargs=1,
        help="Category to plot, e.g. 'dwelling' or 'beds'.")
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    args = parser.parse_args()

    main()
