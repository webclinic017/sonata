#!/usr/bin/python
#-*- coding: utf-8 -*- 

import pandas as pd

class Ticks:
    """
    tick数据结果
    """
    COLUMNS = ['time', 'price', 'volume', 'type']

    def __init__(self):
        #完整代码
        self.symbol = ''
        #ticks数据
        self.df = pd.DataFrame(columns = self.COLUMNS)
