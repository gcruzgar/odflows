import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd 

def uk_plot(shp_path, geo_code, df, var_name, title, cmap='coolwarm'):
    "Choropleth map of the given variable."

    print("\nGenerating plot...")

    map_df = gpd.read_file(shp_path)
    merged = map_df.merge(df[var_name], left_on=geo_code, right_on=df.index, how='left').dropna(subset=[var_name])

    fig, ax = plt.subplots(1,1, figsize=(8,7))
    ax.axis('off')
    ax.set_title(title)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(merged[str(var_name)]),vmax=max(merged[str(var_name)])))
    sm._A = []
    fig.colorbar(sm)
    merged.plot(column=str(var_name), cmap=cmap, linewidth=0.2, edgecolor='0.5', ax=ax)

def top_10(df, var_name, title):
    "Bar chart of the top 10 wards for the given variable"

    df_desc = df.sort_values(by=[var_name], ascending=False)
    plt.figure(figsize=[12,6])
    plt.bar(df_desc.index[0:10], df_desc[var_name][0:10])
    plt.ylabel("Frequency")
    plt.xticks(fontsize=10)
    plt.title(title)

def categ(df, cat, r=False):
    "Most common type of move for a given category in each ward."

    if r == False:
        cat_types = {
            'beds': ['Beds1to3', 'Beds4Plus'], 
            'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached'], 
            'price': ['MovesUnder250k', 'MovesOver250k']
        }
    else:
        cat_types = {
            'beds': ['Beds1to3', 'Beds4Plus'], 
            'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached'], #, 'Bungalow'
            'price': ['RentUnder250', 'RentOver250']
        }

    # most common type in each ward
    df[cat] = df[cat_types[cat]].idxmax(axis=1)

    return df
    
def categ_plot(shp_path, geo_code, df, var_name, title):
    "Categorical plot for given variable"
    print("\nGenerating plot...")
    
    map_df = gpd.read_file(shp_path) 
    merged = map_df.merge(df[var_name], left_on=geo_code, right_on=df.index, how='left').fillna(value='no data available') #.dropna(subset=[var_name]) 
    merged=merged.loc[~merged[geo_code].str.startswith('S', na=False)] # drop Scottish wards

    ax = plt.subplots(1,1, figsize=(8,7))[1]
    ax.axis('off')
    ax.set_title(title)

    merged.plot(column=var_name, cmap='tab20c', categorical=True, legend=True, ax=ax)

def ward_distance(df, map_df):
    """
    Calculate the distance (as the crow flies) between ward centroids.
    Note: this requires a shapefile that contains all wards present in df (UK).
    """
    print("Calculating distances...")

    dist_list = []
    for i in df.index:

        a = df['OriginWardCode'][i]                 # ward code
        ai = map_df.loc[map_df['wd16cd']==a].index  # find index of first ward
        ma = map_df['geometry'][ai.item()]          # find geometry of first ward
        mac = ma.centroid                           # centre point of first ward

        b = df['DestinationWardCode'][i]            # ward code
        bi = map_df.loc[map_df['wd16cd']==b].index  # find index of second ward
        mb = map_df['geometry'][bi.item()]          # find geometry of second ward       
        mbc = mb.centroid                           # centre point of second ward

        ab = mac.distance(mbc)                      # distance between centroids
        dist_list.append(ab)             

    #df['distance'] = dist_list
    #df.to_csv("data/rentals_and_distance.csv")

    return dist_list

def ru_class(remap=True):
    """rural/urban classification of wards according to 2011 ONS census"""

    rural_urban = pd.read_csv("data/Rural_Urban_Classification_2011_of_Wards_in_England_and_Wales.csv")
    #print(rural_urban['RUC11'].value_counts())

    ru_map = {
        'Rural village and dispersed': 'Rural', 'Rural village and dispersed in a sparse setting': 'Rural', 
        'Rural town and fringe': 'Rural', 'Rural town and fringe in a sparse setting': 'Rural',
        'Urban major conurbation':'Urban', 'Urban minor conurbation':'Urban',
        'Urban city and town':'Urban', 'Urban city and town in a sparse setting': 'Urban'
    }
    if remap == True:
        rural_urban['RUC11'].replace(ru_map, inplace=True)

    # plot
    # shp_path = "data/shapefiles/EW_Wards_2011.shp"
    # categ_plot(shp_path, 'geo_code', rural_urban.set_index('WD11CD'), 'RUC11', 'Rural/Urban Classification - 2011')
    # plt.show()

    # merge with df
    #b = df.merge(rural_urban[['WD11CD','RUC11']], left_on='OriginWardCode', right_on=['WD11CD'], how='left')
    #b.to_csv("data/rentals_distance_ru.csv")

    return rural_urban

def Ward_to_LAD(df, df_types):
    
    map_df = gpd.read_file("data/shapefiles/GB_Wards_2016.shp") 
    merged = map_df.merge(df, left_on='wd16cd', right_on=df.index, how='left')
    merged=merged.loc[~merged['wd16cd'].str.startswith('S', na=False)] # drop Scottish wards

    # aggregate to LADs
    lad_map = pd.pivot_table(merged, values=df_types, index='lad16cd', aggfunc=np.sum)
    
    return lad_map 

def load_moves(r=False):
    """ Load sales or rental data.
    Note: the path to data files might need to be changed depedning on how data is stored."""

    if r:
        rs = 'rentals'
        print("Loading rental data...")
        df = pd.read_csv("data/ZooplaRentals_Aggregate_NikLomax.txt", sep='\t')
        df.rename(index=str, columns={'NumberOfRentals': 'Total'}, inplace=True)
        df_types = ['Total', 'RentUnder250', 'RentOver250',
            'Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow', 'PropertyTypeUnknown', 
            'Beds1to3', 'Beds4Plus']
    else:
        rs = 'sales'
        print("Loading sales data...")
        df = pd.read_csv("data/ZooplaSales_Aggregate_NikLomax.txt", sep='\t')
        df.rename(index=str, columns={'NumberOfMoves': 'Total'}, inplace=True)   
        df_types = ['Total', 'MovesUnder250k', 'MovesOver250k', 
            'Terraced', 'Flat', 'SemiDetached', 'Detached',
            'Beds1to3', 'Beds4Plus']

    return df, df_types, rs
