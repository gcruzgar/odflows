#!/usr/bin/env python3
import argparse
import pandas as pd 
import matplotlib.pyplot as plt 

def main():

    if args.r:   
        df = pd.read_csv("data/rentals_and_distance.csv", index_col=0)
        df_types = {
            'beds': ['Beds1to3', 'Beds4Plus'], 
            'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached', 'Bungalow'], 
            'price': ['RentUnder250', 'RentOver250'],
        }
    else:
        df = pd.read_csv("data/sales_and_distance.csv", index_col=0)
        df_types = {
            'beds': ['Beds1to3', 'Beds4Plus'], 
            'dwelling': ['Terraced', 'Flat', 'SemiDetached', 'Detached'], 
            'price': ['MovesUnder250k', 'MovesOver250k'],
        }

    # if args.c[0] == 'RUC11'
    #     df = pd.read_csv("data/sales_distance_ru.csv")
    #     df_types = {
    #         'RUC11': ['Rural', 'Urban']
    #     }
    
    typ = args.c[0]

    d={}
    i=1
    for cat in df_types[typ]:
        
        #df1 = df.loc[df['RUC11']==cat]
        _=plt.subplot(3,2,i)
        _=plt.hist(df['distance']/(1000), bins=500 ,weights=df[cat], cumulative=False, density=True) #weights=df['NumberOfMoves'] if RUC11
        _=plt.xlim([0, 80])
        _=plt.xlabel("Distance (km)")
        _=plt.ylabel("Frequency (%)")
        _=plt.title(cat)

        df1 = df.loc[df[cat]>0]
        d[cat] = (df1['distance']*df1[cat]).mean() #'NumberOfMoves'

        i+=1

    distance_av = pd.Series(d)
    print("\nAverage distance (km): \n{}".format((distance_av/1000).round(2)))

    plt.show()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_true',
        help="use rental data.")
    parser.add_argument("-c", type=str, nargs=1, default=['dwelling'], 
        help="Category to plot: 'beds', 'dwelling', 'price' or 'RUC11'.")
    args = parser.parse_args()

    main()