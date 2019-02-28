import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv("data/rentals_and_distance.csv", index_col=0)
df_types = {
    'beds': ['Beds1to3', 'Beds4Plus'], 
    'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow'], 
    'price': ['RentUnder250', 'RentOver250'],
}

# df = pd.read_csv("data/sales_and_distance.csv", index_col=0)
# df_types = {
#     'beds': ['Beds1to3', 'Beds4Plus'], 
#     'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached'], 
#     'price': ['MovesUnder250k', 'MovesOver250k'],
# }

# df = pd.read_csv("data/sales_distance_ru.csv")
# df_types= {
#     'RUC11': ['Rural', 'Urban']
# }

d={}
i=1
for cat in df_types['dwelling']:
    
    #df1 = df.loc[df['RUC11']==cat]
    _=plt.subplot(3,2,i)
    _=plt.hist(df['distance']/(1000), bins=500 ,weights=df[cat], cumulative=False, normed=True) #weights=df['NumberOfMoves'] if RUC11
    _=plt.xlim([0, 80])
    _=plt.xlabel("Distance (km)")
    _=plt.ylabel("Frequency (%)")
    _=plt.title(cat)

    d[cat] = (df['distance']*df[cat]).mean() #'NumberOfMoves'

    i+=1

distance_av = pd.Series(d)
print("\nAverage distance (km): \n{}".format((distance_av/1000).round(2)))

plt.show()
