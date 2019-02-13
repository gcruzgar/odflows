import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd 

def uk_plot(shp_path, df, var_name, title):

    print("\nGenerating plot...")

    map_df = gpd.read_file(shp_path)
    merged = map_df.set_index("wd16nm").join(df[var_name]).fillna(value=0)

    fig, ax = plt.subplots(1,1, figsize=(8,7))
    ax.axis('off')
    ax.set_title(title)

    sm = plt.cm.ScalarMappable(cmap="OrRd", norm=plt.Normalize(vmin=min(merged[str(var_name)]),vmax=max(merged[str(var_name)])))
    sm._A = []
    fig.colorbar(sm)
    merged.plot(column=str(var_name), cmap='OrRd', linewidth=0.3, edgecolor='0.8', ax=ax)

def top_10(df, var_name, title):
    
    df_desc = df.sort_values(by=[var_name], ascending=False)
    plt.figure(figsize=[12,6])
    plt.bar(df_desc.index[0:10], df_desc[var_name][0:10])
    plt.ylabel("Frequency")
    plt.xticks(fontsize=10)
    plt.title(title)

def categ_plot(shp_path, df, var_name, title):

    print("\nGenerating plot...")
    
    map_df = gpd.read_file(shp_path)
    merged = map_df.set_index("wd16nm").join(df[var_name]).fillna(value='no data available')

    fig, ax = plt.subplots(1,1, figsize=(8,7))
    ax.axis('off')
    ax.set_title(title)

    merged.plot(column=var_name, cmap='tab20c', categorical=True, legend=True, ax=ax)
