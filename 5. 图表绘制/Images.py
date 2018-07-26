# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as mfm
import matplotlib.gridspec as gridspec
import matplotlib.ticker as plticker

class Image(object):
    font_path = {}
    prop = {}
    font_path['hei'] = './font/MSYHMONO.ttf'
    font_path['english'] = './font/Calibri.ttf'
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
        image_path=None, title_y=1.1, xticks_rotation='horizontal', legend_name=[]):
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
        self.set_xticks()
        # 为后续添加副轴留出空间
        self.add_ax()
        self.add_title()
        self.plot()
        self.set_spines()
        self.set_tick_marks()
        self.add_legend()
        # 为后续补充设定留出空间
        self.config_add()
        self.tight_layout()
        self.set_grid()
        plt.close()

    def add_ax(self):
        pass

    def add_legend(self):
        if not (self.legend_name is None):
            self.ax.legend(self.legend_name, loc='upper right', bbox_to_anchor=(1, 1.2), prop=self.legend_font, frameon=True)

    def tight_layout(self, **karg):
        self.gs.tight_layout(self.fig, **karg)

    def plot(self):
        rects = plt.bar(self.x, self.y, 0.4, zorder=3, color=self.default_colors['blue'])
        for rect in rects:
            height = rect.get_height()
            self.ax.text(rect.get_x() + rect.get_width()/2., 1.05*height, 
                        '%d' % int(height), 
                        ha='center', va='bottom')
    def add_title(self):
        if self.title:
            self.ax.set_title(self.title, fontproperties=self.title_font, y=self.title_y)

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

    def set_spines(self):
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
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
            
    def config_add(self):
        """
        保留用于扩展功能或者设定
        """
        pass