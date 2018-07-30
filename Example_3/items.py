# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import logging

from configs import filepath, date, bd, author
from ImageFactory import ImageMultiLine, ImageBar
from datapipeline import product_data

class Product(object):
    def __init__(self, data):
        self.data = data

product = Product(product_data)

class TopList(object):
    def __init__(self, data):
        self.data = data
        self.product_id = self.data['product_id']
        self.price = Price(self.data.groupby(['product_id'])['lowest_price'].mean())
        self.review = Review(self.data)
        self.commodity = Commodity(self.data)
        self.brand = Brand(self.data)

class Price(object):
    def __init__(self, data):
        self.data = data
        self.mean = np.nanmean(self.data)
        self.max = np.max(self.data)
        self.min = np.min(self.data)
        self.count = len(self.data)
        self.space = 5
        self.table = self.distribution_table(50, space=self.space)
        # self.image = self.plot_distribution()
    
    @property    
    def image(self):
        labels = ["\\"+label for label in self.table['labels']]
        image = ImageBar(data=self.table['count'],
                        labels=labels,
                        title='榜单商品价格分布',
                        xticks_rotation=0,
                        legend_name=['商品数量'])
        image.init()
        return image

    def distribution_table(self,
                          truncation_number:int,
                          space_auto=True,
                          space=10,
                          space_power=1,
                          unit_symbol='$'
                          ):
        """
        把数据划分出不同区间，然后计算各个区间的频率

        Parameters
        ----------
        truncation_number : 图表截断值，即区间范围的最大值
        space_auto : 是否自动确定组间距离
        space : 组间距离，即各个区间的范围
        space_power : 组间距离乘数，本身组间距离的增大方式为：当组间距离<=5时，每次加1，当>5时，每次加5
                      二档组间距离乘数为100时，则当组间距离<=500时，每次加100，当>500时，每次加500
        unit_symbol : x轴标签的单位符号，当unit_symbol='$'，x轴0-10区间的标签为$0-$10
                      而当unit_symbol='$'，x轴0-10区间的标签为0-10
        """

        repeat_times = 0
        while True:
            data_last = 0
            data_count = {}
            labels = []
            for data in range(0, int(self.max+1), space):
                if data < truncation_number:
                    data_count['{}{}-{}{}'.format(unit_symbol, data_last, unit_symbol, data)]\
                    = sum((self.data < data) & (self.data >= data_last))
                    data_last = data
                else:
                    data_count['{}{}以上'.format(unit_symbol, truncation_number)]\
                    = sum((self.data >= truncation_number))

            if space_auto:
                if sum(map(lambda x : x != 0, data_count.values()))>14:
                    space += 1*space_power if space<5*space_power else 5*space_power
                elif sum(map(lambda x : x != 0, data_count.values()))>8:
                    break
                else:
                    space -= 1*space_power if space<5*space_power else 5*space_power

                repeat_times += 1
                if repeat_times > 30:
                    logging.warning("循环次数过多，无法自动确认组间距")
                    break
            else:
                break

        if sum(map(lambda x : x != 0, data_count.values()))>14:
            logging.warning("存在分组数大于14，请手动调节组间距和最大截断值")
        df_data = pd.DataFrame({'labels':list(data_count.keys()), 
                                'count':list(data_count.values())}
                               )

        df_data = df_data.dropna()
        df_data = df_data[df_data['count'] != 0]
        return df_data.assign(percentage = lambda x: x['count']/sum(x['count']))

class Review(object):
    def __init__(self, data):
        self.data = data.groupby(['product_id'])['review_count'].mean()
        self.review_rating = data[data['review_count']!=0].review_rating
        self.rating_mean = np.nanmean(self.review_rating)
        self.mean = np.nanmean(self.data)
        self.max = np.max(self.data)
        self.min = np.min(self.data)
        self.sum = np.sum(self.data)
        self.count = len(self.data)

        # self.distribution_table = Price.distribution_table
        try:
            if self.mean>1000:
                self.table = self.distribution_table(10000,
                                                    space=500,
                                                    space_power=100,
                                                    unit_symbol='')
            else:
                self.table = self.distribution_table(1000,
                                                    space=50,
                                                    space_power=2,
                                                    space_auto = True,
                                                    unit_symbol='')
        except BaseException as e:
            print(e)

    def distribution_table(self, *arg, **karg):
        return Price.distribution_table(self, *arg, **karg)

    @property
    def image(self):
        labels = self.table['labels']
        image = ImageBar(data=self.table['count'],
                        labels=labels,
                        title='榜单商品评论数分布',
                        xticks_rotation=20,
                        legend_name=['商品数量']
                        )
        image.init()
        return image

class Commodity(object):
    show_number = 5
    def __init__(self, data):
        self.data = data
        self.product_id = self.data['product_id']
        self.set = set(self.data['product_id'])
        self.count = len(self.set)
        self.table = self.commodity_rank()
        self.rank_change_table = (
            self.data[
            self.product_id.isin(
                self.cp['product_id'].head(self.show_number)
                )
            ].pivot_table(
                index = ['date'],
                columns = ['product_id'],
                values = ['rank']
                )['rank'][self.cp['product_id'].head(self.show_number)]
            )[self.table['ASIN'].head()]
        
    @property
    def image(self):
        image = ImageMultiLine(data=self.rank_change_table,
                       labels=self.rank_change_table.index,
                       title='商品排名变化情况',
                       xticks_rotation=0,
                       title_y = 1.1
                      )
        image.init()
        if image.intervals<1:
            image.intervals = 1
        image.init()
        image.ax.invert_yaxis()
        return image

    def commodity_rank(self):
        groups = self.data.groupby(['product_id'])
        # 上榜次数
        cp_count = pd.DataFrame(groups['date'].nunique())
        # 计算每个商品的平均bsr
        cp_mean = pd.DataFrame(groups['rank'].mean())
        #计算各个商品的最好bsr
        cp_min = pd.DataFrame(groups['rank'].min())
        # 整理成一个表
        self.cp = pd.merge(cp_min.reset_index(),
                      pd.merge(cp_count.reset_index(),
                               cp_mean.reset_index(),
                               on = 'product_id'),
                      on = 'product_id')
        # 对列进行命名
        self.cp.columns = ['product_id','highest_rank','counts','avg_rank']
        # 根据平均排名进行排序
        self.cp = self.cp.sort_values(['counts','avg_rank'],ascending = (False,True))
        # 合并所需要的商品排行表
        self.cp = pd.merge(self.cp,product.data,on = 'product_id')
        
        rank_form = self.cp[['product_id', 'image_url', 'counts', 'avg_rank', 'highest_rank', 'brand', 'review_count', 'review_rating','lowest_price']].head(self.show_number).copy()
        rank_form.index = range(1,self.show_number + 1)
        # 将图片链接改为在html中可以直接显示的类型
        for i in range(len(rank_form)):
            if rank_form.image_url.notnull()[i + 1]:
                if "images-na.ssl" in rank_form.loc[i+1, 'image_url']:
                    rank_form.loc[i+1, 'image_url'] = '<img src = "' + rank_form.image_url[i + 1]\
                     + '"/>'
                # 遇到图片缺失的情况时的处理
                else:
                    logging.warning("ASIN -> {} : Can't get image_url, save url as {}.jpg instead".format(rank_form.product_id, rank_form.product_id))
                    rank_form.loc[i+1, 'image_url'] = '<img src = "' + rank_form.product_id[i + 1]\
                     + '"/>'
        #调整小数位数
        rank_form.avg_rank = rank_form.avg_rank.round(2)

        rank_form.columns = ['ASIN', '图片', '登榜次数', '平均排名', '最高排名', '品牌', '评论量', '平均星级', '当前价格($)']
        return rank_form

class Brand(object):
    show_number = 5
    def __init__(self, data):
        self.data = data
        self.set = set(self.data['brand'])
        self.count = len(self.set)
        self.table = self.commodity_rank()
        self.count_change_table = self.count_change()
        
    @property
    def image(self):
        image = ImageMultiLine(data=self.count_change_table,
                       labels=self.count_change_table.index,
                       title='品牌登榜商品数变化情况',
                       xticks_rotation=0,
                       title_y = 1.1
                      )
        image.init()
        if image.intervals<1:
            image.intervals = 1
        image.init()
        return image

    def count_change(self):
        df_brand_product_counts = pd.DataFrame(self.data.groupby(['brand','date'])['product_id'].count()).reset_index()
        df_brand_productcounts_change = df_brand_product_counts[df_brand_product_counts['brand'].isin(self.table['品牌'].head())].pivot_table(index = ['date'],columns = ['brand'],values = ['product_id'])
        try:
            df_brand_productcounts_change.columns = df_brand_productcounts_change.columns.levels[1]
        except:
            print('')
        df_brand_productcounts_change = df_brand_productcounts_change[self.table['品牌'].head()]
        return df_brand_productcounts_change.fillna(0)

    def commodity_rank(self):
        product.data_id = pd.DataFrame({'product_id':list(set(list(self.data['product_id'])))})
        df_cp_product = pd.merge(product.data_id,product.data,on = 'product_id')
        cp_count = pd.DataFrame(self.data.groupby(['brand'])['rank'].count())
        cp_mean = pd.DataFrame(self.data.groupby(['brand'])['rank'].mean()).round(2)
        cp_productcount = pd.DataFrame(df_cp_product.groupby(['brand'])['product_id'].count())
        cp_max = pd.DataFrame(self.data.groupby(['brand'])['rank'].min())
        cp_reviewcount = pd.DataFrame(df_cp_product.groupby(['brand'])['review_count'].sum()).fillna(0).astype(int)
        cp_reviewrating = pd.DataFrame(df_cp_product[df_cp_product['review_rating']!= 0].groupby(['brand'])['review_rating'].mean()).round(2)
        cp_price = pd.DataFrame(df_cp_product.groupby(['brand'])['lowest_price'].mean()).round(2)
        cp = pd.merge(cp_count.reset_index(),cp_mean.reset_index(),on = 'brand')
        cp = pd.merge(cp,cp_productcount.reset_index(),on = 'brand')
        cp = pd.merge(cp,cp_max.reset_index(),on = 'brand')
        cp = pd.merge(cp,cp_reviewcount.reset_index(),on = 'brand')
        cp = pd.merge(cp,cp_reviewrating.reset_index(),on = 'brand', how = 'outer')
        cp = pd.merge(cp,cp_price.reset_index(),on = 'brand')
        cp.columns = ['brand','counts','avg_rank','prodcut_count','max_rank','review_count','avg_rating','avg_price']
        cp = cp.sort_values(['counts','avg_rank'],ascending = (False,True))
        cp[['brand','counts','prodcut_count','avg_rank','max_rank','review_count','avg_rating','avg_price']].head(self.show_number)
        rank_form = cp[['brand','counts','prodcut_count','avg_rank','max_rank','review_count','avg_rating','avg_price']].head(self.show_number)
        rank_form['avg_price'] = rank_form['avg_price'].map(lambda x:float('%.2f' % x))
        rank_form.columns = ['品牌', '登榜次数', '登榜商品数', '平均排名', '最高排名', '评论量', '平均星级', '平均价格($)']
        rank_form.index = range(1,self.show_number + 1)
        return rank_form


