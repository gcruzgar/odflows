#!/usr/bin/env python3
import argparse
import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 

def main():

    if args.r:
        df = pd.read_csv("data/rentals_and_distance.csv", index_col=0)
        df_types = {
            'beds': ['Beds1to3', 'Beds4Plus'], 
            'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow'], 
            'price': ['RentUnder250', 'RentOver250']
        }
    else:
        df = pd.read_csv("data/sales_and_distance.csv", index_col=0)
        df_types = {
            'beds': ['Beds1to3', 'Beds4Plus'], 
            'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached'], 
            'price': ['MovesUnder250k', 'MovesOver250k']
        }

    typ = args.c[0]
    print("Category: %s" % typ)
    # most common type in each ward
    df['Class'] = df[df_types[typ]].idxmax(axis=1)

    # filter by category
    d = {}
    for cat in df_types[typ]:
        d[cat] = df.loc[df['Class'] == cat, 'distance'].mean()
    distance_av = pd.Series(d)
    print("Average distance (km): \n{}".format((distance_av/1000).round(2)))
    
    return distance_av

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    parser.add_argument("-c", type=str, nargs=1, default=['dwelling'], 
        help="Category to plot: 'beds', 'dwelling' or 'price'.")
    args = parser.parse_args()

    main()
