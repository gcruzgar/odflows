#!/usr/bin/env python3
import argparse
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from utils import categ, categ_plot, ru_class

def main():

    if args.r:
        print("Loading rental data...")
        df = pd.read_csv("data/ZooplaRentals_Aggregate_NikLomax.txt", sep='\t')
        df.rename(index=str, columns={'NumberOfRentals': 'Total'}, inplace=True)
        df_types = ['Total', 'RentUnder250', 'RentOver250',
            'Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow', 'PropertyTypeUnknown', 
            'Beds1to3', 'Beds4Plus']
    else:
        print("Loading sales data...")
        df = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t')
        df.rename(index=str, columns={'NumberOfMoves': 'Total'}, inplace=True)   
        df_types = ['Total', 'MovesUnder250k', 'MovesOver250k', 
            'Terraced', 'Flat', 'SemiDetached', 'Detached',
            'Beds1to3', 'Beds4Plus']

    rural_urban = ru_class()

    b = df.merge(rural_urban[['WD11CD','RUC11']], left_on=['OriginWardCode'], right_on=['WD11CD'], how='left')

    shp_path = "data/shapefiles/GB_Wards_2015.shp"
    cat = args.c[0]

    for ruc in ['Rural', 'Urban']:

        r_df = b.loc[b['RUC11']==ruc]

        odm = pd.pivot_table(r_df, values = df_types, index = 'DestinationWardName', aggfunc=np.sum)
          
        cat_df = categ(odm, cat, args.r)

        categ_plot(shp_path,cat_df, cat, 'Most common %s - %s' % (cat, ruc))
    plt.show()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    parser.add_argument("-c", type=str, nargs=1, default=['dwelling'], 
        help="Category to plot: 'beds', 'dwelling', 'price' or 'RUC11'.")
    args = parser.parse_args()

    main()
