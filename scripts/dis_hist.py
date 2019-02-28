import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv("data/rentals_and_distance.csv", index_col=0)
df_types = {
    'beds': ['Beds1to3', 'Beds4Plus'], 
    'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow'], 
    'price': ['RentUnder250', 'RentOver250'],
    'RUC11': ['Rural', 'Urban']
}

# df = pd.read_csv("data/sales_and_distance.csv", index_col=0)
# df_types = {
#     'beds': ['Beds1to3', 'Beds4Plus'], 
#     'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached'], 
#     'price': ['MovesUnder250k', 'MovesOver250k'],
# }

d={}
i=1
for cat in df_types['dwelling']:
    
    plt.subplot(3,2,i)
    _=plt.hist(df['distance']/(1000), bins=300 ,weights=df[cat], cumulative=False, normed=True)
    plt.xlim([0, 80])
    plt.xlabel("Distance (km)")
    plt.ylabel("Frequency (%)")
    plt.title(cat)

    d[cat] = (df['distance']*df[cat]).mean()

    i+=1

distance_av = pd.Series(d)
print("\nAverage distance (km): \n{}".format((distance_av/1000).round(2)))

plt.show()
