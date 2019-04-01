#!/usr/bin/env python3
import numpy as np 
import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
from utils import uk_plot

def main():
    """ Load UK green-space data, aggregate to Ward and plot. 
    Data is available in deciles, with 1 meaning best performing and 10 worst, and in raw amount."""
    
    LSOA_Ward = pd.read_csv("data/EW_LSOA_Ward_Lookup_2016.csv")
    ahah = pd.read_csv("data/ahahinputs.csv")

    green_space = ahah[['lsoa11', 'green900_decile']] #'green900'

    gs_ward = green_space.merge(LSOA_Ward, left_on='lsoa11', right_on='LSOA11CD', how='left')

    gs_df = pd.pivot_table(gs_ward, values = ['green900_decile'], index = 'WD16CD', aggfunc=np.mean) # how to aggregate?

    shp_path = "data/shapefiles/GB_Wards_2016.shp"
    geo_code = 'wd16cd'

    uk_plot(shp_path, geo_code, gs_df, 'green900_decile', 'average green space decile', cmap='Greens_r')
    plt.show()

    migration = pd.read_csv("data/sales_destination_ward_2016.csv").set_index('DestinationWardCode')  #.set_index('Unnamed: 0') #.set_index(OriginWardCode)

    migration_perc = migration.drop(columns=['Total']).div(migration['Total'], axis=0) * 100

    merged = gs_df.merge(migration, left_on='WD16CD', right_on=migration.index).set_index('WD16CD')
    merged_perc = gs_df.merge(migration_perc, left_on='WD16CD', right_on=migration_perc.index).set_index('WD16CD')

    corr_df = merged.corr()
    print(corr_df.iloc[0].round(3))

if __name__ == "__main__":
    
    main()