#!/usr/bin/env python3
import argparse
import numpy as np 
import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
from utils import uk_plot, top_10, categ, categ_plot, load_moves

def main():

    var_name = args.var_name
    df, df_types, rs = load_moves(r=args.r) # Load flow data
    df.dropna(subset=['DestinationWardCode'], inplace=True) # Only keep data with both origin and destination

    # Note: dropna is used to only keep available od pairs

    df_dict = {
        'df_origin': pd.pivot_table(df, values = df_types, index = 'OriginWardCode', aggfunc=np.sum),
        'df_destination': pd.pivot_table(df, values = df_types, index = 'DestinationWardCode', aggfunc=np.sum),
    }
    df_dict['df_net'] = df_dict['df_destination'] - df_dict['df_origin']

    print("\nMoves from origin: \n{}".format(df_dict['df_origin'].sum()))
    print("\nMoves to destination: \n{}".format(df_dict['df_destination'].sum()))

    shp_path = "data/shapefiles/GB_Wards_2016.shp"
    geo_code = 'wd16cd'

    # raw - net
    uk_plot(shp_path, geo_code, df_dict['df_net'], var_name, 'net df - '+var_name)
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
        cat_df = categ(df_dict['df_origin'], cat, args.r)
        categ_plot(shp_path, geo_code, cat_df, cat, ('Most frequent %s - %s' % (rs, cat)))

    plt.show()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default="Total",
        help="Variable to plot, e.g. 'Total' or 'Beds1to3'.")
    parser.add_argument("-c", type=str, nargs=1,
        help="Category to plot: 'beds', 'dwelling' or 'price'.")
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    args = parser.parse_args()

    main()
