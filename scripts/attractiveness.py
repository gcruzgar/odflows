#!/usr/bin/env python3
import pandas as pd 
import numpy as np
import argparse

def green_space(g_type='green900_decile'):
    """Load green space data. Aggregates LSOA data to Ward. Can use either raw value (m-squared) or deciles. 
    Note: wards can vary greatly in size so aggregating on raw green space would require normalising based on size or similar."""  

    LSOA_Ward = pd.read_csv("data/EW_LSOA_Ward_Lookup_2016.csv")
    ahah = pd.read_csv("data/ahahinputs.csv")

    green_space = ahah[['lsoa11', g_type]] 

    gs_ward = green_space.merge(LSOA_Ward, left_on='lsoa11', right_on='LSOA11CD', how='left')

    gs_df = pd.pivot_table(gs_ward, values = [g_type], index = 'WD16CD', aggfunc=np.mean)

    return gs_df

def main():

    factor = args.c[0]
    factor = factor.title()
    print(factor)

    factors = {
        'Crime': pd.read_csv("data/Burglary_ward_2016.csv").set_index('WD16CD').rename(index=str, columns={'Crime rate': 'Crime'}),
        'Green': green_space().rename(index=str, columns={'green900_decile': 'Green'})
    }

    df = factors[factor]

    sales = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t') # load sales data

    merged = sales.merge(df, left_on='OriginWardCode', right_on=df.index) # create new column with factor value at origin ward
    merged.rename(index=str, columns={factor: 'Origin'+factor}, inplace=True) # rename column

    merged = merged.merge(df, left_on='DestinationWardCode', right_on=df.index) # create new column with factor value at destination ward
    merged.rename(index=str, columns={factor: 'Destination'+factor}, inplace=True) # rename column

    merged[factor+' difference'] = merged['Destination'+factor] - merged['Origin'+factor] # create new column with difference between destination and origin

    df_types = ['NumberOfMoves', 'MovesUnder250k', 'MovesOver250k', 
        'Terraced', 'Flat', 'SemiDetached', 'Detached',
        'Beds1to3', 'Beds4Plus',
        factor+' difference']

    df_corr = merged[df_types].corr()
    print(df_corr[factor+' difference'].round(3)[:-1])

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", type=str, nargs=1, default=["crime"], 
        help="Attractiveness factor: 'crime' or 'green'.")
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    args = parser.parse_args()

    main()
