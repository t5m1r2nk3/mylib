# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 14:20:07 2022

@author: pc
"""
#%%サンキーズを書く関数
import pandas as pd
import numpy as np
import plotly.graph_objects as go
def draw_sk(s_df,s_file_name,title_name):
#カラム名の変更
    s_df.columns = ['source_name', 'target_name', 'value']

# sourceのユニーク値をリスト化
    lst_name = s_df['source_name'].unique().tolist()
# targetのユニーク値もリスト化し、上で作成したリストに結合
    lst_name.extend(s_df['target_name'].unique().tolist())
# 結合したリスト内の重複要素を削除
    lst_name = sorted(set(lst_name), key=lst_name.index)
# lst_nameと同じ要素数で連番のリストを作成（[0, 1, …, x]）
    lst_num = list(range(len(lst_name)))


########################
# source, targetという列を新たに作成
    s_df[['source', 'target']] = np.nan

########################　sourceとtargetの列に、lst_numで定義した連番の数値を入力  ########################

# =============================================================================
#     for i in ['source', 'target']:
#         for j, k in zip(lst_name, lst_num):
#             s_df[i].mask(s_df[str(i) + '_name'] == j, k, inplace=True)
# =============================================================================
    for i in ['source', 'target']:
        for j, k in zip(lst_name, lst_num):
            s_df[i] = s_df[i].mask(s_df[str(i) + '_name'] == j, k)

        
 
######################## sankey図のリンクのカラーを指定する ########################
    s_df['link_color'] = 'rgba(125, 125, 125, 0.3)'#←デフォルト、rgba(216, 216, 216, 0.8)は薄い

    fig = go.Figure(data=[go.Sankey(
#    arrangement='snap',
    node=dict(
        #font=30,#もとは20font_size=30
        
        pad=5,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=lst_name,
#         x=[0.2, 0.5, 0.6, 0.5, 0.6, 0.5, 0.6, 0.2, 0.9, 0.9, 0.9, 0.9, 0.9],
#         y=[0.6, 0.4, 0.4, 0.9, 0.9, 0.8, 0.8, 0.1, 0.9, 0.8, 0.5, 0.3, 0.1],
        color='lightskyblue'
        
             #color=["blue", "blue", "green", "green"]
    ),
    link=dict(
        source=s_df['source'],
        target=s_df['target'],
        value=s_df['value'],
        color=s_df['link_color']
    ))])

    #fig.update_layout(title_text=title_name,font_size=30)
    fig.update_layout(title_text=title_name,font=dict(size=70))#1個目がタイトルのフォントサイズ、２個目が之ノードラベルのフォントサイズ
    # レイアウトの設定
    fig.update_layout(
        title=dict(
            text=title_name,
            font=dict(size=40)  # タイトルのフォントサイズ
        ),
        font=dict(size=20)  # ノードラベルのフォントサイズ
    )
    fig.show()
    fig.write_html(s_file_name, auto_open=False)
    

def goukei(g_df):
    g_df.columns = ['source_name', 'target_name', 'value']
#souce_name
    for i in ['source','target'] :
        tmp_g_df=g_df.loc[:,[i+'_name','value']] 
        df_l_sum=tmp_g_df.groupby([i+'_name']).sum()
        df_l_sum['合計']=round(df_l_sum['value']/1000,1)
        df_l_sum['合計']='【'+ df_l_sum['合計'].astype(str) +'】'
        df_l_sum.drop(columns=['value'],inplace=True)
        df_l_sum.reset_index(inplace=True)
        g_df=pd.merge(g_df,df_l_sum, on=i+'_name',how='left')
        g_df[i+'_name']=g_df[i+'_name']+g_df['合計']
        g_df.drop(columns=['合計'],inplace=True)

    #仮の変数削除
    del df_l_sum
    return g_df


#%%↓以下の関数はgoukeiと同じ（３列以上に対応？）
def fukusuu(s_df,summ):
    tmp_df=pd.DataFrame(columns=['source_name', 'target_name','value'])
    for i in range(len(s_df.columns)-2):
        tmp_df2=s_df.iloc[:,[i,i+1,len(s_df.columns)-1]].set_axis(['source_name', 'target_name', 'value'], axis=1)
        #合計整理(合計値がいらないときは###)
        if summ==1:
            tmp_df2=goukei(tmp_df2)
        #データ結合
        #tmp_df=pd.concat([tmp_df,tmp_df2],axis=0)
        #tmp_df = pd.concat([tmp_df, tmp_df2.dropna(axis=1, how='all')], axis=0)
        tmp_df = pd.concat([tmp_df, tmp_df2.loc[:, tmp_df2.notna().any()]], axis=0)



    return tmp_df
    del tmp_df,tmp_df2

if __name__ == '__main__':
    print('scriptから実行')
    
#念のため保存    
# =============================================================================
# def fukusuu(s_df):
#     tmp_df=pd.DataFrame(columns=['source_name', 'target_name','value'])
#     for i in range(len(s_df.columns)-2):
#         tmp_df2=s_df.iloc[:,[i,i+1,len(s_df.columns)-1]].set_axis(['source_name', 'target_name', 'value'], axis=1)
#         #合計整理(合計値がいらないときは###)
#         tmp_df2=goukei(tmp_df2)
#         #データ結合
#         tmp_df=pd.concat([tmp_df,tmp_df2],axis=0)
# 
#     return tmp_df
#     del tmp_df,tmp_df2
# =============================================================================
    
    
#%%

def draw_sk_excel(s_df,s_file_name,title_name):
    # sourceのユニーク値をリスト化
    lst_name =s_df['source_name'].unique().tolist()
    # targetのユニーク値もリスト化し、上で作成したリストに結合
    lst_name.extend(s_df['target_name'].unique().tolist())
    # 結合したリスト内の重複要素を削除
    lst_name = sorted(set(lst_name), key=lst_name.index)

#うまく動いていた
    fig = go.Figure(data=[go.Sankey(node=dict(pad=5,thickness=20,line=dict(color='black', width=0.5),label=lst_name,color='rgba(176, 199, 213,1)'),#color='lightskyblue'←デフォルト、'rgba(176, 199, 213,1)'は薄い
                                    link=dict(source=s_df['source'],target=s_df['target'],value=s_df['value'],color=s_df['link_color']))])
    

    fig.update_layout(title_text=title_name,font_size=30)#font_size=20
    fig.show()
    fig.write_html(s_file_name, auto_open=False)
    
    
    







