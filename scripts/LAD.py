#!/usr/bin/env python3
import argparse
import numpy as np 
import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
from utils import uk_plot, categ, categ_plot, load_moves

def main():

    df, df_types, rs = load_moves(r=args.r)

    if args.f == 'net':
        cmap='coolwarm'
        df = df.dropna(subset=['DestinationWardCode'])
    else:
        cmap='OrRd'
        
    df_dict = {
        'origin': pd.pivot_table(df, values = df_types, index = 'OriginWardCode', aggfunc=np.sum),
        'destination': pd.pivot_table(df, values = df_types, index = 'DestinationWardCode', aggfunc=np.sum),
    }
    df_dict['net'] = df_dict['destination'] - df_dict['origin']

    target = args.f  

    map_df = gpd.read_file("data/shapefiles/GB_Wards_2016.shp") 
    merged = map_df.merge(df_dict[target], left_on='wd16cd', right_on=df_dict[target].index, how='left')
    merged=merged.loc[~merged['wd16cd'].str.startswith('S', na=False)] # drop Scottish wards

    # aggregate to LADs
    lad_map = pd.pivot_table(merged, values=df_types, index='lad16cd', aggfunc=np.sum)

    shp_path = "data/shapefiles/GB_LAD_2016.shp"
    geo_code = 'lad16cd'

    # plots
    var_name = args.var_name
    uk_plot(shp_path, geo_code, lad_map, var_name, '%s-flow - %s %s' % (target, var_name, rs), cmap)

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
    parser.add_argument("-c", type=str, nargs=1, default=["dwelling"], 
        help="Category to plot: 'beds', 'dwelling' or 'price'.")
    parser.add_argument("-f", type=str, nargs='?', default="origin",
        help="flow of interest: 'origin', 'destination', or 'net'.")
    args = parser.parse_args()
    main()