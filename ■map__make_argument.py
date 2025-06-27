"""s_columns:表示させたい数字のあるデータベースの列
city_columns:市町村のあるデータベースの列
c_map:カラーマップ
s_df:s_columnsのあるデータベース
s_k:切り分ける数、整数
s_file_name:保存名
title_name:タイトル名
legend_title:凡例のタイトル
"""

#%%category
city_columns='表明市町村'
s_columns='表明'
c_map='ocean'
s_df=df
s_k=1
s_file_name='E:\\category_test.png'
title_name='二酸化炭素ゼロ表明市町村'
legend_title='二酸化炭素ゼロ表明市町村'

map_make.map_category(city_columns,s_columns,c_map,s_df,s_k,s_file_name,title_name,legend_title)

#%%BAR
city_columns='排出市町村'
s_columns='トン換算数量'
c_map='YlOrRd_r'
s_df=df
s_file_name='E:\\bar_test.png'
title_name='タイトル名テスト'
legend_title='凡例タイトルテスト'

map_make.map_bar(city_columns,s_columns,c_map,s_df,s_file_name,title_name,legend_title)

#%%_difine

city_columns='排出市町村'
s_columns='トン換算数量'
c_map='YlOrRd_r'
s_df=df
s_file_name='E:\\bar_test.png'
title_name='タイトル名テスト'
legend_title='凡例タイトルテスト'
#まずはcategoryで閾値のめぼしと最大値を確認してからs_binとlabelを決めるとよい
s_bins=[10000,80000]
s_labels=['0-10000','10000-80000']

map_make.map_difine(city_columns,s_columns,c_map,s_df,s_file_name,title_name,legend_title,s_bins,s_labels)
