#!/usr/bin/env python3
import argparse
import numpy as np 
import pandas as pd 
import geopandas as gpd 
from utils import uk_plot, top_10, load_moves
import matplotlib.pyplot as plt 

def main():

    var_name = args.var_name

    df, df_types, rs = load_moves(r=args.r)

    print("Total frequency: \n{}".format(df.iloc[:,4:].sum())) 

    df_dict = {'df_origin': pd.pivot_table(df, values = df_types, index = 'OriginWardCode', aggfunc=np.sum), 
        'df_destination': pd.pivot_table(df, values = df_types, index = 'DestinationWardCode', aggfunc=np.sum),
    }

    print("\nMoves from origin: \n{}".format(df_dict['df_origin'].sum()))
    print("\nMoves to destination: \n{}".format(df_dict['df_destination'].sum()))

    # Plots
    shp_path = "data/shapefiles/GB_Wards_2016.shp"
    geo_code = "wd16cd"

    if var_name != 'Total':
        pc_df_origin =  df_dict['df_origin'].drop(columns=['Total']).div(df_dict['df_origin']['Total'], axis=0)
        pc_df_destination = df_dict['df_destination'].drop(columns=['Total']).div(df_dict['df_destination']['Total'], axis=0)

        uk_plot(shp_path, geo_code, pc_df_origin, var_name, 'df_origin - '+var_name+' '+rs+' - net normalised', 'OrRd')
        uk_plot(shp_path, geo_code, pc_df_destination, var_name, 'df_destination - '+var_name+' '+rs+' - net normalised', 'OrRd')
        #top_10(pc_df_net,var_name, var_name+' (net normalised) - Top 10')
    else:
        for key in df_dict:
            df = df_dict[key]
            title = key+' - '+var_name+' '+rs
            uk_plot(shp_path, geo_code, df, var_name, title, 'OrRd')
            #top_10(df,var_name, title)

    plt.show()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default="Total",
        help="Variable to plot, e.g. 'Total' or 'Beds1to3'.")
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    args = parser.parse_args()
    
    main()
