#!/usr/bin/env python3
import pandas as pd 
import numpy as np 

df = pd.read_csv("data/UKvarR.csv")
#df.head()
#df.columns

odm = pd.pivot_table(df, values = 'Flow', index = 'Dest', columns = ['Ori'], fill_value=0)
total_out = odm.sum(axis=0).rename('total_out') 
total_in = odm.sum(axis=1).rename('total_in') 

var_list = ['Ori', 'Dest', 'Flow', 'ContiguityDum', 'Offset', 'Distance', 'OriPop',
       'DestPop', 'OriDens', 'DestDens', 'PcUnempOri', 'PcUnempDest',
       'PcRentOri', 'PcRentDest', 'PcNonNatOri', 'PcNonNatDest', 'PcDegreeOri',
       'PcDegreeDest', 'PcIllOri', 'PcIllDest', 'DepRatioOri', 'DepRatioDest',
       'PcMarriedOri', 'PcMarriedDest']

attraction_vars = ['DestPop', 'DestDens', 'PcUnempDest', 'PcRentDest', 'PcNonNatDest',
       'PcDegreeDest', 'PcIllDest', 'DepRatioDest', 'PcMarriedDest']

emission_vars = ['OriPop', 'OriDens', 'PcUnempOri', 'PcRentOri', 'PcNonNatOri',
       'PcDegreeOri', 'PcIllOri', 'DepRatioOri', 'PcMarriedOri']

print("\ncorrelation of destination factors with migration flow to destination:")
for att in attraction_vars:
    
    att_df = pd.pivot_table(df, values = att, index = 'Dest')
    f_df = pd.concat([total_in, att_df], axis=1, join='inner')
    fc = f_df.corr()
    print("%s: %0.3f" % (att, fc.loc[att][0]))

print("\ncorrelation of origin factors with flow from origin:")
for em in emission_vars:
    
    em_df = pd.pivot_table(df, values = em, index = 'Ori')
    f_df = pd.concat([total_out, em_df], axis=1, join='inner')
    fc = f_df.corr()
    print("%s: %0.3f" % (em, fc.loc[em][0]))

a = df[['Distance', 'Flow']]
a = a.loc[a['Flow'] != 0]
print("\nDistance: %0.3f" % a.corr().iloc[0,1])