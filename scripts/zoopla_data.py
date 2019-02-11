#!/usr/bin/env python3
import argparse
import numpy as np 
import pandas as pd 
import geopandas as gpd 
from utils import uk_plot, top_10
import matplotlib.pyplot as plt 

def main():

    var_name = args.var_name
    
    #rentals = pd.read_csv("data/ZooplaRentals_Aggregate_NikLomax.txt", sep='\t')
    sales = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t')    

    #print(rentals.iloc[:,4:].sum())
    print(sales.iloc[:,4:].sum())  

    sales_types = ['NumberOfMoves', 'MovesUnder250k', 'MovesOver250k', 
        'Terraced', 'Flat', 'SemiDetached', 'Detached',
        'Beds1to3', 'Beds4Plus']
    #rental_types = ['NumberOfRentals', 'RentUnder250', 'RentOver250',
    #    'Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow', 'PropertyTypeUnknown', 
    #    'Beds1to3', 'Beds4Plus']

    # Plots
    #if
    df_dict = {'sales_origin': pd.pivot_table(sales, values = sales_types, index = 'OriginWardName', aggfunc=np.sum), 
        'sales_destination': pd.pivot_table(sales, values = sales_types, index = 'DestinationWardName', aggfunc=np.sum),
    }
    #df_dict['sales_net'] =  df_dict['sales_destination'] - df_dict['sales_origin'] 
    # df_dict = {
    #     'rentals_origin': pd.pivot_table(rentals, values = rental_types, index = 'OriginWardName', aggfunc=np.sum), 
    #     'rentals_destination': pd.pivot_table(rentals, values = rental_types, index = 'DestinationWardName', aggfunc=np.sum)
    # }

    shp_path = "data/shapefiles/UK_Wards_2016.shp"

    for key in df_dict:
        
        df = df_dict[key]
        title = key+' - '+var_name
        uk_plot(shp_path, df, var_name, title)
        top_10(df,var_name, title)
    plt.show()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default="NumberOfMoves",
        help="Variable to plot, e.g. 'NumberOfMoves' or 'Beds1to3'.")
    args = parser.parse_args()
    
    main()
