#%データセット
import pandas as pd
import sys
import os
import copy
import numpy as np
import geopandas as gpd
import matplotlib.colors
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import mapclassify
import japanize_matplotlib

#%地図データ取得
import gcsfs

df_city = gpd.read_file('gs://map_niwa/geojson/hokkaido_city.geojson')
df_sinkou = gpd.read_file('gs://map_niwa/geojson/hokkaido_sinkoukyoku.geojson')
df_hoppou = gpd.read_file('gs://map_niwa/geojson/hokkaido_hoppou.geojson')

#%###############################カテゴリー###############################
def map_category(city_columns,s_columns,c_map,s_df,s_k,s_file_name,title_name,legend_title):

    df_map_merge=pd.merge(df_city, s_df, left_on='N03_004', right_on=city_columns,how='left')

    #データ空白地区なくす
    df_map_merge[s_columns]=df_map_merge[s_columns].fillna(0)

    fig = plt.figure(figsize=(16,8),dpi=150)#ディフォルト8,6
    ax = fig.add_subplot(111)
    ax.axis("off")
    legend_kwds = dict(bbox_to_anchor=(0.7, 0.85), loc='upper left', borderaxespad=0,#bbox_to_anchor=(0.7, 0.45)
                       fontsize=10,frameon = False,fmt='{:.0f}',#.0f:整数
                       #labels=['0-20%','20-40%','40-60%','60-80%','80-104%'],
                       title=legend_title,title_fontsize=10)
    # scheme="quantiles"カテゴリー
    base= df_map_merge.plot(column=s_columns, cmap=c_map ,
                   legend=True,
                   scheme="quantiles", k=s_k,
                   #scheme="User_Defined", k=6,
                   legend_kwds = legend_kwds,
                   #classification_kwds=dict(bins=[20,40,60,80,104]),
                   edgecolor='black', linewidth=0.1)
    base.set_title(title_name, fontsize=14)
    #北方領土追加
    ax = df_hoppou.plot(column="N03_001",legend=False, legend_kwds=legend_kwds,ax=base,  color='white')
    #振興局境界線追加
    ax = df_sinkou.plot(ax=base, color='none', edgecolor='k', linewidth=0.5)
    #市町村境界線追加
    ax = df_city.plot(ax=base, color='none', edgecolor='k', linewidth=0.1)
    ax.axis("off")
    plt.savefig(s_file_name, format="png", dpi=300)

###############################BAR#########################################
def map_bar(city_columns,s_columns,c_map,s_df,s_file_name,title_name,legend_title):
    fig = plt.figure(figsize=(8,6),dpi=150)#facecolor='darkgray'
    ax = fig.add_subplot(111)
    ax.axis("off")
    df_map_merge=pd.merge(df_city, s_df, left_on='N03_004', right_on=city_columns,how='left')

    #データ空白地区なくす
    df_map_merge[s_columns]=df_map_merge[s_columns].fillna(0)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="1%", pad=-1)
    base =df_map_merge.plot(column=s_columns,ax=ax, cmap=c_map ,cax=cax,legend=True,facecolor='white', edgecolor='black', linewidth=0.1,
                legend_kwds={"label":legend_title,"fmt":'{:,d}'},
                #vmin=0, vmax=10000
                )

    base.set_title(title_name, fontsize=10)
    #北方領土追加
    ax = df_hoppou.plot(column="N03_001",legend=False, ax=base,  color='white')
    #振興局境界線追加
    ax = df_sinkou.plot(ax=base, color='none', edgecolor='k', linewidth=0.2)
    #市町村境界線追加
    ax = df_city.plot(ax=base, color='none', edgecolor='k', linewidth=0.1)
    ax.axis("off")
    plt.savefig(s_file_name, format="png", dpi=300)

###############################凡例と閾値任意#########################################
def map_difine(city_columns,s_columns,c_map,s_df,s_file_name,title_name,legend_title,s_bins,s_labels):

    df_map_merge=pd.merge(df_city, s_df, left_on='N03_004', right_on=city_columns,how='left')

    #データ空白地区なくす
    df_map_merge[s_columns]=df_map_merge[s_columns].fillna(0)

    fig = plt.figure(figsize=(8,6),dpi=150)
    ax = fig.add_subplot(111)
    ax.axis("off")
    legend_kwds = dict(bbox_to_anchor=(0.70, 0.50), loc='upper left', borderaxespad=0,labels=s_labels,#bbox_to_anchor=(0.65, 0.4)
                       title=legend_title,fontsize=10,frameon = False,title_fontsize=10,fmt='{:,.0f}')
    # scheme="quantiles"カテゴリー
    base= df_map_merge.plot(column=s_columns, cmap=c_map ,
                   legend=True,#legend=True
                   scheme="User_Defined",
                   legend_kwds = legend_kwds,
                   classification_kwds=dict(bins=s_bins),
                   edgecolor='black', linewidth=0.1)
    base.set_title(title_name, fontsize=12)

    #北方領土追加
    #ax = df_hoppou.plot(column="N03_001",legend=False, legend_kwds=legend_kwds,ax=base,  color='white')
    #振興局境界線追加
    ax = df_sinkou.plot(ax=base, color='none', edgecolor='k', linewidth=0.2)#linewidth=0.2,0.5
    #市町村境界線追加
    ax = df_city.plot(ax=base, color='none', edgecolor='k', linewidth=0.1)
    ax.axis("off")
    plt.savefig(s_file_name, format="png", dpi=300)