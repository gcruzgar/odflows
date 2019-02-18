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
    distance_list.append(sales.loc[sales['dwelling'] == cat, 'distance'].mean())
print(list(zip(sales_types['dwelling'], distance_list)))
