#!/usr/bin/env python3
import argparse
import numpy as np 
import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
from utils import uk_plot, top_10, categ_plot

def categ(df, cat):

    cat_types = {
        'beds': ['Beds1to3', 'Beds4Plus'], 
        'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached'], 
        'price': ['MovesUnder250k', 'MovesOver250k']
    }
    
    # most common type in each ward
    df[cat] = df[cat_types[cat]].idxmax(axis=1)

    return df

def main():

    var_name = args.var_name

    sales = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t').dropna(axis=0, how='any')

    sales_types = ['NumberOfMoves', 'MovesUnder250k', 'MovesOver250k', 
        'Terraced', 'Flat', 'SemiDetached', 'Detached',
        'Beds1to3', 'Beds4Plus']

    sales_origin = pd.pivot_table(sales, values = sales_types, index = 'OriginWardName', aggfunc=np.sum)
    sales_destination = pd.pivot_table(sales, values = sales_types, index = 'DestinationWardName', aggfunc=np.sum)
    sales_net = sales_destination - sales_origin

    print("\nMoves from origin: \n{}".format(sales_origin.sum()))
    print("\nMoves to destination: \n{}".format(sales_destination.sum()))

    shp_path = "data/shapefiles/UK_Wards_2016.shp"

    # raw - net
    uk_plot(shp_path, sales_net, var_name, 'net sales - '+var_name)
    #top_10(sales_net,var_name, var_name+' (net) - Top 10')

    # normalised
    if var_name != 'NumberOfMoves':
        pc_sales_origin =  sales_origin.drop(columns=['NumberOfMoves']).div(sales_origin['NumberOfMoves'], axis=0)
        pc_sales_destination = sales_destination.drop(columns=['NumberOfMoves']).div(sales_destination['NumberOfMoves'], axis=0)
        pc_sales_net = pc_sales_destination - pc_sales_origin

        uk_plot(shp_path, pc_sales_net, var_name, 'sales - '+var_name+' - net normalised')
        #top_10(pc_sales_net,var_name, var_name+' (net normalised) - Top 10')
            
    # categorical
    cat = args.c[0]
    cat_df = categ(sales_origin, cat)
    categ_plot(shp_path, cat_df, cat, 'Most frequent - '+cat)

    plt.show()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default="NumberOfMoves",
        help="Variable to plot, e.g. 'NumberOfMoves' or 'Beds1to3'.")
    parser.add_argument("-c", type=str, nargs=1, default="dwelling",
        help="Category to plot, e.g. 'dwelling' or 'beds'.")
    args = parser.parse_args()

    main()
