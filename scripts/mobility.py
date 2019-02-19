#!/usr/bin/env python3
import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
from utils import uk_plot, categ_plot

rentals = pd.read_csv("data/rentals_and_distance.csv", index_col=0)
sales = pd.read_csv("data/sales_and_distance.csv", index_col=0)

sales_types = {
    'beds': ['Beds1to3', 'Beds4Plus'], 
    'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached'], 
    'price': ['MovesUnder250k', 'MovesOver250k']
}

rentals_types = {
    'beds': ['Beds1to3', 'Beds4Plus'], 
    'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow'], 
    'price': ['RentUnder250', 'RentOver250']
}

# most common type in each ward
sales['dwelling'] = sales[sales_types['dwelling']].idxmax(axis=1)

# filter by category
distance_list = []
for cat in sales_types['dwelling']:
    distance_list.append((cat, [sales.loc[sales['dwelling'] == cat, 'distance'].mean()]))
distance_list = pd.DataFrame.from_items(distance_list)
print("Average distance (m): \n{}".format(distance_list.round(2)))

#rural/urban classification
rural_urban = pd.read_csv("data/Rural_Urban_Classification_2011_of_Wards_in_England_and_Wales.csv")
#print(rural_urban['RUC11'].value_counts())

ru_map = {
    'Rural village and dispersed': 'Rural', 'Rural village and dispersed in a sparse setting': 'Rural', 
    'Rural town and fringe': 'Rural', 'Rural town and fringe in a sparse setting': 'Rural',
    'Urban major conurbation':'Urban', 'Urban minor conurbation':'Urban',
    'Urban city and town':'Urban', 'Urban city and town in a sparse setting': 'Urban'
}
rural_urban['RUC11'].replace(ru_map, inplace=True)

shp_path = "data/shapefiles/GB_Wards_2015.shp"
categ_plot(shp_path, rural_urban.set_index('WD11NM'), 'RUC11', 'Rural/Urban split - 2011')
plt.show()
