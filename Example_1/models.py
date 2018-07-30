# -*- coding: utf-8 -*-
import logging

class Document(object):
    def __init__(self):
        # 文章标题
        self.title = None
        # 子标题
        self.subtitle = None
        # 前言
        self.foreword = None
        # 章节
        self.chapters = []
        for i in range(5):
            self.chapters.append(Chapter(subchapter_number=4, number="chapter{}".format(i)))

    def print_structure(self, deep):
        if self.chapters:
            for subchapter in self.chapters:
                print('--'*deep+subchapter.number)
                subchapter.print_structure(deep+1)
        else:
            return

class Chapter(Document):
    def __init__(self, subchapter_number=0, number=''):
        """
        subchapter_number : 子章节数
        number : 章节编号，基于文档结构生成，需要是唯一的
        """
        self.title = None
        self.content1 = None
        self.table = None
        # 图表会先做出图片形式，此处保存图片的路径
        self.image = None
        self.content2 = None
        self.rank_list_change = None
        self.number = number
        self.chapters= [Chapter(subchapter_number=0, number="{}_subchapter{}".format(self.number, i)) 
                           for i in range(subchapter_number)]
        # 设定图片保存的链接
        self.image_path = './image/'
        

    def set_image(self, fig):
        image_filename = '{}{}.png'.format(self.image_path, self.number)
        fig.savefig(image_filename, dpi=160, bbox_inches='tight')
        self.image = image_filename

    def __getattr__(self, name):
        try:
            return self.name
        except:
            logging.error("Attribute is not exist")
            return None
        
# 子章节定义可以直接使用Chapter定义，利用了Python类的继承，也为之后补充自定义子章节提供了留白
class Subchapter(Chapter):
    pass