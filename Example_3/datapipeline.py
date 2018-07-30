# -*- coding: utf-8 -*-
import pandas as pd
from configs import bd, date, filepath, report_name
   
def read_data():
    df = pd.read_pickle('./reports/{}/data/{}{}_product.pkl'.format(
        report_name, bd, date))
    # 修复价格显示百倍
    df.loc[:, 'lowest_price'] = df['lowest_price']/100
    return df

product_data = read_data()
     
def read_list_data(list_name):
    df_ = pd.read_pickle('./reports/{}/data/{}{}_{}.pkl'.format(report_name, bd, date, list_name))
    df = pd.merge(df_, product_data, how='left', on = 'product_id')
    return df

list_data = {}
for list_name in ['bestsellers', 'hotnewreleases', 'moversandshakers']:
    list_data[list_name] =  read_list_data(list_name)