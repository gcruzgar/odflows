#!/usr/bin/env python3
import argparse
import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
from utils import ru_class

def main():

    if args.r:
        df = pd.read_csv("data/rentals_and_distance.csv", index_col=0)
        df_types = {
            'beds': ['Beds1to3', 'Beds4Plus'], 
            'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow'], 
            'price': ['RentUnder250', 'RentOver250'],
            'RUC11': ['Rural', 'Urban']
        }
        norm_type = 'NumberOfRentals'
    else:
        df = pd.read_csv("data/sales_and_distance.csv", index_col=0)
        df_types = {
            'beds': ['Beds1to3', 'Beds4Plus'], 
            'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached'], 
            'price': ['MovesUnder250k', 'MovesOver250k'],
            'RUC11': ['Rural', 'Urban']
        }
        norm_type='NumberOfMoves'

    typ = args.c[0]
    print("Category: %s" % typ)
    # most common type in each ward
    if typ != 'RUC11':
        df['Class'] = df[df_types[typ]].idxmax(axis=1)
    else:
        rural_urban = ru_class()
        df = df.merge(rural_urban[['WD11CD','RUC11']], left_on='OriginWardCode', right_on=['WD11CD'], how='left')
        df.rename(index=str, columns={'RUC11': 'Class'}, inplace=True)

    # filter by category
    d = {}
    dw={}
    for cat in df_types[typ]:
        d[cat] = df.loc[df['Class'] == cat, 'distance'].mean()
        
        if typ != 'RUC11':
            dw[cat] = (df['distance']*df[cat]).mean()
        else:
            df1 = df.loc[df['Class'] == cat]
            dw[cat] = (df1['distance']*df1[norm_type]).mean()
        
    distance_av = pd.Series(d)
    distance_wav = pd.Series(dw)
    print("Average distance (km): \n{}".format((distance_av/1000).round(2)))
    print("\nAverage weighted distance (km): \n{}".format((distance_wav/1000).round(2)))
    return distance_av

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    parser.add_argument("-c", type=str, nargs=1, default=['dwelling'], 
        help="Category to plot: 'beds', 'dwelling', 'price' or 'RUC11'.")
    args = parser.parse_args()

    main()
