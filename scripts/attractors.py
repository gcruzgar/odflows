#!/usr/bin/env python3
import argparse
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from utils import categ, categ_plot, ru_class

def main():
    """
    This script loads sales or rental OD flows, aggregated by ward.
    It then filters data such that only moves originating from rural (or only urban) areas remain.
    From the remaining data, the total flow into each ward is calculated.
    Finally, it plots the most common category (e.g. dwelling type) for each ward based on the type of property from which it originates.
    Note: there is no information on the property each person ends up in, only which one they sold/rented. 
    
    The same can be done but filtering moves based on the destination being rural and calculating total flows out of each ward.
    """

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

    if args.of:
        in_out = 'destination'
        print("total outflow")
        od_a = 'DestinationWardCode'
        od_b = 'OriginWardName'
    else:
        in_out = 'origin'
        print("total inflow")
        od_a = 'OriginWardCode'
        od_b = 'DestinationWardName'

    rural_urban = ru_class()
    # classify moves as rural or urban based on their origin/destination ward
    b = df.merge(rural_urban[['WD11CD','RUC11']], left_on=[od_a], right_on=['WD11CD'], how='left')

    shp_path = "data/shapefiles/GB_Wards_2015.shp"
    cat = args.c[0]

    for ruc in ['Rural', 'Urban']:

        r_df = b.loc[b['RUC11']==ruc] # filter moves based on origin/destination being rural or urban

        odm = pd.pivot_table(r_df, values = df_types, index = od_b, aggfunc=np.sum)
          
        cat_df = categ(odm, cat, args.r) # 
        print("\nNumber of moves with %s areas as %s: " % (ruc, in_out))
        print(cat_df[cat].value_counts())
        categ_plot(shp_path,cat_df, cat, 'Most common %s - %s %s' % (cat, ruc, in_out))
    plt.show()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    parser.add_argument("-c", type=str, nargs=1, default=['dwelling'], 
        help="Category to plot: 'beds', 'dwelling', 'price' or 'RUC11'.")
    parser.add_argument("-of", action='store_true',
        help="show outflow (total moves into wards).")
    args = parser.parse_args()

    main()
