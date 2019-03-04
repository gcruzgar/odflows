#!/usr/bin/env python3
import argparse
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from utils import categ, categ_plot

def main():

    if args.r:
        print("Loading rental data...")
        df = pd.read_csv("data/rentals_distance_ru.csv")
        df.rename(index=str, columns={'NumberOfRentals': 'Total'}, inplace=True)
        df_types = ['Total', 'RentUnder250', 'RentOver250',
            'Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow', 'PropertyTypeUnknown', 
            'Beds1to3', 'Beds4Plus']
    else:
        print("Loading sales data...")
        df = pd.read_csv("data/sales_distance_ru.csv")
        df.rename(index=str, columns={'NumberOfMoves': 'Total'}, inplace=True)   
        df_types = ['Total', 'MovesUnder250k', 'MovesOver250k', 
            'Terraced', 'Flat', 'SemiDetached', 'Detached',
            'Beds1to3', 'Beds4Plus']

    ruc = args.ruc[0]
    r_df = df.loc[df['RUC11']==ruc]
    r_df = pd.pivot_table(r_df, values = df_types, index = 'OriginWardName', aggfunc=np.sum)

    cat = args.c[0]
    cat_df = categ(r_df, cat, args.r)

    shp_path = "data/shapefiles/GB_Wards_2015.shp"

    categ_plot(shp_path,cat_df, cat, 'Most common dwelling - %s' % ruc)
    plt.show()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    parser.add_argument("-ruc", type=str, nargs=1, default=['Rural'],
        help="Rural or Urban")
    parser.add_argument("-c", type=str, nargs=1, default=['dwelling'], 
        help="Category to plot: 'beds', 'dwelling', 'price' or 'RUC11'.")
    args = parser.parse_args()

    main()
