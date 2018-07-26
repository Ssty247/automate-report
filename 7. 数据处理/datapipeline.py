import pandas as pd
import numpy as np

from tools import str2num

converters = {'Price':str2num,
              'Rank':str2num,
              'Rating':str2num,
              'Sales':str2num,
              'Revenue':str2num,
              'Reviews':str2num
             }
try:
    data = pd.read_csv('data.csv', converters=converters, header=7, index_col=0)
except BaseException as e:
    print(e)