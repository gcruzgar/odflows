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

## crime data 
# crime = pd.read_csv("data/Burglary_LAD_2016.csv")
# migration = pd.read_csv("data/sales_LAD_2016.csv").drop(columns=['dwelling']).set_index('lad16cd')

# migration_perc = migration.drop(columns=['Total']).div(migration['Total'], axis=0) * 100

# merged = crime.merge(migration, left_on='lad16cd', right_on=migration.index).set_index('lad16cd')
# merged_perc = crime.merge(migration_perc, left_on='lad16cd', right_on=migration_perc.index).set_index('lad16cd')

# corr_df = merged_perc.corr()
# print(corr_df.iloc[0].round(3))
##

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_true',
        help="use rental data.")    
    args = parser.parse_args()

    main()
