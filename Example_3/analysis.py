# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import logging

from datapipeline import product_data, list_data
from items import product, TopList

lists = {'Best Seller':TopList(list_data['bestsellers']), 
         'Hot New Releases':TopList(list_data['hotnewreleases']), 
         'Movers & Shakers':TopList(list_data['moversandshakers'])}
bs = lists['Best Seller']
hnr = lists['Hot New Releases']
mns = lists['Movers & Shakers']


class Info(object):
    def __init__(self):
        self.rank_lists = list(lists.values())
        self.review_total_count = sum([rank_list.review.sum for rank_list in self.rank_lists])
        sorted_time = sorted(list(set(bs.data['date'])))
        start_time = sorted_time[0]
        self.start_time = str(start_time.year) + '年' + str(start_time.month) + '月' + str(start_time.day) + '日'
        end_time = sorted_time[-1]
        self.end_time = str(end_time.year) + '年' + str(end_time.month) + '月' + str(end_time.day) + '日'
        self.category_name = bs.data['dept_name'][0]

    @property
    def commodity_total_count(self): 
        commodity_total = bs.commodity.set and hnr.commodity.set and mns.commodity.set
        commodity_total_count = len(commodity_total)
        return commodity_total_count
        
    @property
    def brand_total_count(self): 
        brand_total = bs.brand.set and hnr.brand.set and mns.brand.set
        brand_total_count = len(brand_total)
        return brand_total_count
    
    @property
    def rating_mean(self):
        rating = np.array([rank_list.review.rating_mean for rank_list in self.rank_lists])
        count = np.array([rank_list.review.count for rank_list in self.rank_lists])
        rating_mean = np.dot(rating, count)/np.sum(count)
        return rating_mean

info = Info()