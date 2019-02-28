# odflows

This repository is unfished. WIP

Exploratory analysis of dwelling rentals and sales in England and Wales.

Number of sales and rentals in dataset, percentage of total in brackets:

|Property listings   |Number of Sales    |Number of Rentals | 
|--------------------|------------------:|-----------------:| 
|Total               | 1,828,646         | 1,204,913        | 
|Moves Under £250(k for sales) | 1,198,034 (65.5%) |   820,210 (68.1%)|
|Moves Over £250(k for sales)  |   630,612 (34.5%) |   376,770 (31.3%)|
|Terraced            |   533,248 (29.2%) |   275,711 (22.9%)|
|Flat                |   362,865 (19.8%) |   511,854 (42.5%)|
|SemiDetached        |   482,237 (26.4%) |   136,376 (11.3%)|
|Detached            |   450,296 (24.6%) |    85,247 (7.1%) |
|Bungalow            |         0 (0%)    |    29,977 (2.5%) |
|PropertyTypeUnknown |         0 (0%)    |   165,748 (13.8%)|
|Beds1to3            |   745,708 (40.8%) | 1,012,098 (84.0%)|
|Beds4Plus           |   198,778 (10.9%) |   154,832 (12.9%)|

Approximately 23% of records provided a forwarding postcode, therefore it is possible to obtain origin-destination pairs for 417,219 households sold (145,885 rentals). However, this will heavily bias the data, especially since forwarding is a paid service. The differences between properties listed and those with forwarding postcode can be seen below (percentage change from total in brackets):

| OD pairs          | Sales          | Rent           |
|-------------------|---------------:|---------------:|
|MovesUnder250k     | 54.8% (-10.7%) | 35.5% (-32.6%) | 
|MovesOver250k      | 45.2% (+10.7%) | 64.0% (+32.7%) | 
|Terraced           | 28.6% (-0.6%)  | 21.7% (+1.2%)  | 
|Flat               |  9.7% (-10.1%) | 32.9% (-9.6%)  | 
|SemiDetached       | 29.9% (+3.5%)  | 14.6% (+3.3%)  |
|Detached           | 31.9% (+7.3%)  | 11.6% (+4.5%)  |
|Bungalow           |    0% (+0%)    |  3.6% (+1.1%)  |
|PropertyTypeUnknown|    0% (+0%)    | 15.6% (+1.8%)  |
|Beds1to3           | 44.9% (+4.1%)  | 83.7% (-0.3%)  |
|Beds4Plus          | 19.8% (+8.9%)  | 14.7% (+1.8%)  |

To check: numbers don't match totals. Small errors expected in % due to rounding but raw numbers dont add up. Large discrepancy in bedroom information for sales.

As expected, reducing the data to households with a forwarding service favours more expensive moves. The number of flats in the data also reduces significantly (10%). The changes are larger for rentals than sales, but these are relevant in both cases.

We can compare data between wards to obtain general trends in the data. For example, in figure (1) we can see the most frequent type of dwelling sold in each ward. Although terraced houses are the most common property sold across the UK, these concentrate mainly in urban areas whilst most wards have a higher number of detached properties sold. It is interesting to note that Greater London has a significant number of flats being sold, being more common that terraced.

![sales_dwelling](img/sales_category_dwelling.png)    
**Figure 1.** Most common type of dwelling sold in each ward.

Moves can be split into under or over £250,000 transactions as shown in figure (2). It is common for properties in the UK to be sold over this threshold (35% of total), however, cheaper moves are predominant in the North and East of England as well as in Wales. Price bands should be obtained to gain more insight in this subject. 

![sales_price](img/sales_category_price.png)    
**Figure 2.** Most common price threshold for households sold in each ward.

It is more common for properties to be sold with one to three beds but in several wards properties with four or more are predominant. This pattern appears to be uniform across the UK. 

![sales_beds](img/sales_category_beds.png)    
**Figure 3.** Most common number of bedrooms per household sold in each ward.

Results are very similar when observing rentals instead of sales. The main difference being the increased percentage of flats rented as well as a strong dominance of properties with one to three beds accounting for 80% of data. It is also worth noting that origin-destination pairs are even more skewed, with rents over £250 representing 64% of od pairs compared to 31% of the total rentals listed. 

![rentals_dwelling](img/rentals_category_dwelling.png)    
**Figure 4.** Most common type of dwelling rented in each ward.

![rentals_price](img/rentals_category_price.png)    
**Figure 5.** Most common price threshold for households rented in each ward.

![rentals_beds](img/rentals_category_beds.png)    
**Figure 6.** Most common number of bedrooms per household rented in each ward.

Average distance between origin and destination varies for each type of sale.

Average distance between wards with type as most common:

| Average Distance (km) | Sales | Rentals |
|-----------------------|------:|--------:|
|Terraced               | 45.01 |  42.51  |  
|Flat                   | 45.27 |  42.92  |
|SemiDetached           | 51.80 |  41.62  |
|Detached               | 62.90 |  47.49  |
|Bungalow               | na    |  47.29  |
|Price Under £250 (k for sales)    | 45.31 |  42.79  |
|Price Over £250 (k for sales)     | 60.70 |  44.12  |
|Bedrooms 1-3           | 51.34 | 42.22   |
|Bedrooms 4 or more     | 56.76 | 50.19   |
|Rural                  | 56.64 | 44.30   |
|Urban                  | 49.75 | 42.21   |

The most interesting differences are that detached property sales have a much greater mobility than other types, over 10km difference. More expensive sales also have a greater mobility thatn cheaper ones (around 15km difference) and rural areas move more on average than urban ones.

Average distance between origin and destination:

| Average Distance (km) | Sales | Rentals |
|-----------------------|------:|--------:|
|Terraced               | 14.41 |   9.18  |  
|Flat                   |  4.89 |  15.33  |
|SemiDetached           | 15.36 |   6.18  |
|Detached               | 20.03 |   5.65  |
|Bungalow               | na    |   1.74  |
|Price Under £250 (k for sales)    | 25.60 |  28.80  |
|Price Over £250 (k for sales)     | 29.09 |  16.11  |
|Bedrooms 1-3           | 24.26 |  37.60  |
|Bedrooms 4 or more     | 11.39 |   6.88  |
|Rural                  | 58.71 |  45.84  |
|Urban                  | 52.06 |  44.11  |

It is useful to look at the rural urban classification of wards stated by the ONS (see figure 7). This gives insight into some of the patterns seen in previous figures because cities behave differently to rural areas.

![rural-urban_split](img/rural_urban_split.png)    
**Figure 7.** ONS rural urban classification by ward - 2011 census.

Correlation of moves with distance:     

| Correlation with Distance     | Sales  | Rentals |
|-------------------------------|-------:|--------:|
|Number of Moves                | -0.160 | -0.150  | 
|Price Under £250 (k for sales) | -0.152 | -0.112  | 
|Price Over £250 (k for sales)  | -0.091 | -0.074  | 
|Terraced                       | -0.132 | -0.083  | 
|Flat                           | -0.094 | -0.075  | 
|SemiDetached                   | -0.124 | -0.071  | 
|Detached                       | -0.089 | -0.041  | 
|Bungalow                       |     na | -0.026  | 
|Beds1to3                       | -0.145 | -0.142  | 
|Beds4Plus                      | -0.095 | -0.052  | 

Overall, there is a negative correlation between moves and distance. People are less likely to buy or rent if the destination is further away. However, these correlations are quite weak.
