#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: ticks.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-05-08 23:34
# @ModifyDate: 2016-05-08 23:34
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

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
