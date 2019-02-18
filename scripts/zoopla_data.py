#!/usr/bin/env python3
import argparse
import numpy as np 
import pandas as pd 
import geopandas as gpd 
from utils import uk_plot, top_10
import matplotlib.pyplot as plt 

def main():

    var_name = args.var_name

    if args.r:
        df = pd.read_csv("data/ZooplaRentals_Aggregate_NikLomax.txt", sep='\t')
        df.rename(index=str, columns={'NumberOfRentals': 'Total'}, inplace=True)
        df_types = ['Total', 'RentUnder250', 'RentOver250',
            'Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow', 'PropertyTypeUnknown', 
            'Beds1to3', 'Beds4Plus']
    else:
        df = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t')
        df.rename(index=str, columns={'NumberOfMoves': 'Total'}, inplace=True)   
        df_types = ['Total', 'MovesUnder250k', 'MovesOver250k', 
            'Terraced', 'Flat', 'SemiDetached', 'Detached',
            'Beds1to3', 'Beds4Plus']

    print("Total frequency: \n{}".format(df.iloc[:,4:].sum())) 

    df_dict = {'df_origin': pd.pivot_table(df, values = df_types, index = 'OriginWardName', aggfunc=np.sum), 
        'df_destination': pd.pivot_table(df, values = df_types, index = 'DestinationWardName', aggfunc=np.sum),
    }

    print("\nMoves from origin: \n{}".format(df_dict['df_origin'].sum()))
    print("\nMoves to destination: \n{}".format(df_dict['df_destination'].sum()))

    # Plots
    shp_path = "data/shapefiles/GB_Wards_2015.shp"

    for key in df_dict:
        
        df = df_dict[key]
        title = key+' - '+var_name
        uk_plot(shp_path, df, var_name, title)
        #top_10(df,var_name, title)

    if var_name != 'Total':
        pc_df_origin =  df_dict['df_origin'].drop(columns=['Total']).div(df_dict['df_origin']['Total'], axis=0)
        pc_df_destination = df_dict['df_destination'].drop(columns=['Total']).div(df_dict['df_destination']['Total'], axis=0)

        uk_plot(shp_path, pc_df_origin, var_name, 'df_origin - '+var_name+' - net normalised')
        uk_plot(shp_path, pc_df_destination, var_name, 'df_destination - '+var_name+' - net normalised')
        #top_10(pc_df_net,var_name, var_name+' (net normalised) - Top 10')

    plt.show()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default="Total",
        help="Variable to plot, e.g. 'Total' or 'Beds1to3'.")
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    args = parser.parse_args()
    
    main()
