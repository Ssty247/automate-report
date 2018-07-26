# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as mfm
import matplotlib.gridspec as gridspec
import matplotlib.ticker as plticker
import numpy as np
import types
from itertools import cycle

class Image(object):
    font_path = {}
    prop = {}
    font_path['hei'] = '../font/MSYHMONO.ttf'
    font_path['english'] = '../font/Calibri.ttf'
    for font_name in list(font_path):
        prop[font_name] = mfm.FontProperties(fname=font_path[font_name])

    title_font = prop['hei'].copy()
    title_font.set_size(14)
    xticks_font = prop['hei'].copy()
    xticks_font.set_size(9)
    ylable_font = prop['hei'].copy()
    ylable_font.set_size(10)
    legend_font = prop['hei'].copy()
    legend_font.set_size(9)
    default_colors = {}
    default_colors['blue'] = '#6CADDD'
    default_colors['yellow'] = '#F3903F'
    default_colors['red'] = '#CB615A'
    default_colors['orange'] = '#F3903F'
    default_colors['gray'] = '#B4B4B4'
    default_colors['lightyellow'] = '#FCC900'
    default_colors['royalblue'] = '#5488CF'

    IMAGE_WIDTH = 5.708
    IMAGE_HIGH = 2.756

    def __init__(self, title=None, labels=None, data=None, 
        image_path=None, title_y=1.1, xticks_rotation='vertical', legend_name=[]):
        self.length = len(data)
        self.x = np.arange(self.length)
        self.y = data
        self.data = data
        self.title_y = title_y
        self.title = title
        self.labels = labels
        self.legend_name = legend_name
        self.xticks_rotation = xticks_rotation

    def init(self):
        self.fig = plt.figure(figsize=(self.IMAGE_WIDTH, self.IMAGE_HIGH))
        self.gs = gridspec.GridSpec(1, 1)
        self.ax = self.fig.add_subplot(self.gs[0])
        self.init_plus()
        self.set_margins()
        self.set_xticks()
        self.add_ax()
        self.add_title()
        self.plot()
        self.set_spines()
        self.set_tick_marks()
        self.add_legend()
        self.config_add()
        self.tight_layout()
        self.set_grid()
        plt.close()

    def config_add(self):
        pass

    def add_ax(self):
        pass

    def init_plus(self):
        pass

    def add_legend(self):
        if not (self.legend_name is None):
            if len(self.legend_name)==1:
                plt.legend(self.legend_name, loc='upper right', bbox_to_anchor=(1, 1.2), prop=self.legend_font, frameon=True)
            elif len(self.legend_name)==2:
                lines1, labels1 = self.ax.get_legend_handles_labels()
                self.ax.legend(lines1, labels1, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.2), prop=self.legend_font, frameon=False)


    def set_ylabel(self):
        pass

    def tight_layout(self, **karg):
        self.gs.tight_layout(self.fig, **karg)

    def plot(self):
        self.ax.fill_between(self.x, self.y.min()*0.9, 
                self.y, zorder=3, color=self.default_colors['blue'])        

    def add_title(self):
        if self.title:
            plt.title(self.title, fontproperties=self.title_font, y=self.title_y)

    def set_grid(self):
        get_ax_space = lambda x: x.get_ylim()[1] - x.get_ylim()[0]
        self.ax_space = get_ax_space(self.ax)
        def get_interval(ax_space, space_number=5):
            digit_number = len(str((ax_space)))
            intervals = int((ax_space)/(space_number*(10**digit_number)))
            while intervals == 0:
                digit_number -= 1
                intervals = int((ax_space)/(space_number*(10**digit_number)))
            linshi = round((ax_space)/(space_number*(10**digit_number)))
            intervals = linshi*(10**digit_number)
            return intervals

        if not 'intervals' in self.__dict__.keys():
            self.intervals = get_interval(self.ax_space)
        loc = plticker.MultipleLocator(base=self.intervals)
        self.ax.yaxis.set_major_locator(loc)
        self.ax.grid(axis='y', zorder=0)
        if 'ax2' in self.__dict__.keys():
            print("有双轴需要设置副轴grid")
            self.ax_space2 = get_ax_space(self.ax2)
            self.intervals2 = get_interval(self.ax_space2, space_number=5)
            loc2 = plticker.MultipleLocator(base=self.intervals2)
            self.ax2.yaxis.set_major_locator(loc2)

    def set_margins(self):
        self.ax.margins(0.013, 0.073) 

    def set_spines(self):
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        # self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)

    def set_tick_marks(self):
        self.ax.tick_params(axis='both', which='both', bottom=False, top=False, 
                labelbottom=True, left=False, right=False, labelleft=True)
        
    def set_xticks(self):
        plt.xticks(self.x, self.labels, fontproperties=self.xticks_font, rotation=self.xticks_rotation) # 设置横坐标标签

    def show(self):
        plt.show()

    def save(self):
        if image_path:
            self.fig.savefig(image_path)
        else:
            logging.warning("Please sure image path firse")

class ImageFill(Image):
    # def __init__(self):
    #     pass

    def set_spines(self):
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)

class ImageBar(Image):
    def __init__(self, title=None, labels=None, data=None, image_path=None, xticks_rotation = 40,
                 legend_name=[], y2=None, title_y=1.2):
        self.y2 = y2
        super(ImageBar, self).__init__(title=title, labels=labels, data=data, image_path=image_path, 
            title_y=title_y, xticks_rotation=xticks_rotation, legend_name=legend_name)

    def plot(self):
        rects = plt.bar(self.x, self.y, 0.4, zorder=3, color=self.default_colors['blue'])
        for rect in rects:
            height = rect.get_height()
            self.ax.text(rect.get_x() + rect.get_width()/2., 1.05*height, 
                        '%d' % int(height), 
                        ha='center', va='bottom')

    # def set_xticks(self):
    #     plt.xticks(self.x, self.labels, fontproperties=self.xticks_font, rotation= self.xticks_rotation, wrap=True) 

class ImageTwinx(Image):
    def __init__(self, title=None, labels=None, data=None, image_path=None, xticks_rotation=40, 
                 legend_name=[], y2=None, title_y=1.2, ylabel_show=True):
        self.ylabel_show = ylabel_show
        self.legend_name = legend_name
        self.marker_style = dict(color=self.default_colors['yellow'], linestyle='-', marker='o')
        self.y2 = y2
        super(ImageTwinx, self).__init__(title=title, labels=labels, data=data,
        image_path=image_path, xticks_rotation=xticks_rotation, title_y=title_y, legend_name=legend_name)

    def config_add(self):
        self.set_ylabel()

    def set_ylabel(self):
        if self.ylabel_show:
            self.ax.set_ylabel(self.legend_name[0], fontproperties=self.ylable_font)
            self.ax2.set_ylabel(self.legend_name[1], fontproperties=self.ylable_font)

    def add_ax(self):
        self.ax2 = self.ax.twinx()
        
    def tight_layout(self, **karg):
        self.gs.tight_layout(self.fig, **karg)

    def plot(self):
        self.ln1 = self.ax.bar(self.x, self.y, 0.4, zorder=3, label=self.legend_name[0], color=self.default_colors['blue'])
        self.ax2.plot(self.x, self.y2, label=self.legend_name[1], **self.marker_style)

    def set_spines(self):
        for _ax in [self.ax, self.ax2]:
            _ax.margins(0) # 设置留白
            # spines
            _ax.spines['right'].set_visible(False)
            _ax.spines['top'].set_visible(False)
            _ax.spines['left'].set_visible(False)

    def set_tick_marks(self):
        self.ax.tick_params(axis='both', which='both', bottom=False, top=False, 
            labelbottom=True, left=False, right=False, labelleft=True)
        self.ax2.tick_params(axis='both', which='both', bottom=False, top=False, 
            labelbottom=True, left=False, right=False)

    def add_legend(self):
        if not (self.legend_name is None):
            if len(self.legend_name) == 2:
                lines1, labels1 = self.ax.get_legend_handles_labels()
                lines2, labels2 = self.ax2.get_legend_handles_labels()
                self.ax.legend(lines1+lines2, labels1+labels2, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.27), prop=self.legend_font, frameon=False)

class ImageLine(Image):
    def __init__(self, title=None, labels=None, data=None, image_path=None,  
        title_y = 1.08, xticks_rotation='horizontal', legend_name=[]):
        self.marker_style = dict(color=Image.default_colors['blue'], linestyle='-')
        super(ImageLine, self).__init__(title=title, labels=labels, data=data, 
            image_path=image_path, title_y=title_y, xticks_rotation= xticks_rotation,
            legend_name=legend_name)
        self.init_plus = self.config_add

    def config_add(self):
        self.set_ylabel()
        self.ax.set_ylim(top = round(np.max(self.y)*1.1))

    def plot(self):
        self.ax.plot(self.x, self.y, **self.marker_style)

class ImagePie(Image):
    colors = ['#F3903F','#B4B4B4','#FCC900','#6CADDD',
    '#D9D4CF', '#7C7877', '#ABD0CE', '#F0E5DE', '#6AAFE6', 
    '#D09E88', '#D4DFE6']

    def plot(self):
        self.explode = np.ones(self.length)*0.03
        self.patches = self.ax.pie(self.y, 
            explode=self.explode, 
            labels=self.labels, 
            colors=self.colors, 
            autopct='%d%%')

    def set_grid(self):
        pass

    def add_legend(self):
        handles = []
        for i, l in enumerate(self.labels):
            handles.append(mpl.patches.Patch(color=self.colors[i], label=l))
        self.ax.legend(handles, self.labels, loc="center right", frameon=False)

class ImageFluctuation(ImageTwinx):
    def plot(self):
        self.ax.plot(self.x, self.y, label=self.legend_name[0], **self.marker_style)
        self.ax2.bar(self.x, self.y2, 0.4, zorder=3, label=self.legend_name[1], color=self.default_colors['red'])
        
    def init_plus(self):
        self.marker_style = dict(color=self.default_colors['blue'], linestyle='-')
    
    def set_xticks(self):
        plt.xticks(range(0,self.length,30), self.labels.loc[[0, 30, 60, 90, 120, 150, 180]], fontproperties=self.xticks_font, rotation=self.xticks_rotation)
        
    def set_ylim(self, top=None, bottom=None):
        if not top:
            top=int(np.max(self.y)*1.1)
        if not bottom:
            bottom=int(np.min(self.y)*0.8)
        if top and bottom:
            try:
                self.ax.set_ylim(top=top, bottom=bottom)
            except:
                top=int(np.max(self.y)*1.1)
                bottom=int(np.min(self.y)*0.8)
                self.ax.set_ylim(top=top, bottom=bottom)
        
    def config_add(self):
        self.set_ylabel()
        self.set_ylim()

class ImageDoubleLine(ImageTwinx):
    def init_plus(self):
        self.marker_style1 = dict(color=self.default_colors['red'], linestyle='-')
        self.marker_style2 = dict(color=self.default_colors['blue'], linestyle='-')
    
    def plot(self):
        self.ax.plot(self.x, self.y, label=self.legend_name[0], **self.marker_style1)
        self.ax2.plot(self.x, self.y2, label=self.legend_name[1], **self.marker_style2)
        
    def set_xticks(self):
        plt.xticks(range(0,self.length,30), self.labels.loc[[0, 30, 60, 90, 120, 150, 180]], fontproperties=self.xticks_font, rotation=self.xticks_rotation)

class ImageMultiLine(Image):
    IMAGE_HIGH = 2.756
    color_cycle = cycle(['blue', 'orange', 'red', 'lightyellow', 'royalblue'])

    def plot(self):
        self.marker_style = []
        for asin in self.y.columns:
            data = self.y[asin]
            marker_style = dict(color=self.default_colors[next(self.color_cycle)], 
                                linestyle='-', marker='o')
            self.marker_style.append(marker_style)
            self.ax.plot(self.x, data, zorder=3, label=asin, **marker_style)
            
    def set_tick_marks(self):
        self.ax.tick_params(axis='both', zorder=1, which='both', bottom=True, top=False, 
                labelbottom=True, left=False, right=False, labelleft=False)

    def set_margins(self):
        self.ax.margins(0.013, 0.073) 

    def set_yticks(self):
        self.ax.yaxis.tick_right()
        self.set_tick_marks()

    def config_add(self):
        self.set_yticks()
        data_max = self.y.max().max()
        if round(data_max*1.1)-round(data_max)>1:
            top = round(data_max*1.1)
        else:
            top = round(data_max)+1
        self.ax.set_ylim(top=top)

    def add_legend(self):
        handles, labels = self.ax.get_legend_handles_labels()
        self.ax.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.4), prop=self.legend_font, frameon=False)