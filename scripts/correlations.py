#!/usr/bin/env python3
import pandas as pd 
import argparse

def main():
    
    if args.r:
        r = 'Rentals'
        df = pd.read_csv("data/rentals_and_distance.csv", index_col=0)

        var_list=['NumberOfRentals', 'RentUnder250', 'RentOver250',
            'Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow',
            'PropertyTypeUnknown', 'Beds1to3', 'Beds4Plus', 'distance']
    else:
        r = 'Sales'    
        df = pd.read_csv("data/sales_and_distance.csv", index_col=0)

        var_list = ['NumberOfMoves', 'MovesUnder250k', 'MovesOver250k',
            'Terraced', 'Flat', 'SemiDetached', 'Detached',
            'Beds1to3', 'Beds4Plus', 'distance']

    print("\nCorrelation of %s with distance: " % r)
    df_cor = df[var_list].corr()

    print(df_cor['distance'].round(3)[:-1])

    return df_cor

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_true',
        help="use rental data.")    
    args = parser.parse_args()

    main()
