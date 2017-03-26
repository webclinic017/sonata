#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: quote.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-28 16:08
# @ModifyDate: 2016-04-28 16:08
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.date_time as date_time

class Quote:
    """
    一次报价结果
    """

    def __init__(self):
        #完整代码
        self.symbol = ''
        #股票代码
        #self.code = ''
        #股票名字
        self.name = ''
        #当前价格
        self.now = 0
        #今日开盘价
        self.open = 0
        #昨日收盘价
        self.close = 0
        #今日最高价
        self.high = 0
        #今日最低价
        self.low = 0
        #竞买价，即“买一”报价
        self.buy = 0
        #竞卖价，即“卖一”报价
        self.sell = 0
        #成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百
        self.volume = 0
        #成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万
        self.turnover = 0
        #买一申报量
        self.bid1_volume = 0
        #买一报价
        self.bid1 = 0
        #买二申报量
        self.bid2_volume = 0
        #买二报价
        self.bid2 = 0
        #买三申报量
        self.bid3_volume = 0
        #买三报价
        self.bid3 = 0
        #买四申报量
        self.bid4_volume = 0
        #买四报价
        self.bid4 = 0
        #买五申报量
        self.bid5_volume = 0
        #买五报价
        self.bid5 = 0
        #卖一申报量
        self.ask1_volume = 0
        #卖一报价
        self.ask1 = 0
        #卖二申报量
        self.ask2_volume = 0
        #卖二报价
        self.ask2 = 0
        #卖三申报量
        self.ask3_volume = 0
        #卖三报价
        self.ask3 = 0
        #卖四申报量
        self.ask4_volume = 0
        #卖四报价
        self.ask4 = 0
        #卖五申报量
        self.ask5_volume = 0
        #卖五报价
        self.ask5 = 0
        #日期
        #self.date = date_time.str_to_date('1900-01-01')
        #时间
        self.time = date_time.str_to_time('1900-01-01 00:00:00')
        return

    def __str__(self):
        """
        行情字符串输出
        """
        format = '<symbol:%s, name:%s, now:%.2f, open:%.2f, close:%.2f, high:%.2f, low:%.2f, ' \
                + 'buy:%.2f, sell:%.2f, turnover:%d, volume:%2f, ' \
                + 'b1v:%d, b1:%.2f, b2v:%d, b2:%.2f, b3v:%d, b3:%.2f, b4v:%d, b4:%.2f, b5v:%d, b5:%.2f, ' \
                + 'a1v:%d, a1:%.2f, a2v:%d, a2:%.2f, a3v:%d, a3:%.2f, a4v:%d, a4:%.2f, a5v:%d, a5:%.2f, ' \
                'time:%s>'
        result = format % (self.symbol, self.name, self.now, self.open, self.close, self.high, self.low, \
                    self.buy, self.sell, self.turnover, self.volume, \
                    self.bid1_volume, self.bid1, self.bid2_volume, self.bid2, self.bid3_volume, \
                    self.bid3, self.bid4_volume, self.bid4, self.bid5_volume, self.bid5, \
                    self.ask1_volume, self.ask1, self.ask2_volume, self.ask2, self.ask3_volume, \
                    self.ask3, self.ask4_volume, self.ask4, self.ask5_volume, self.ask5, \
                    date_time.time_to_str(self.time))
                    #date_time.date_to_str(self.date), date_time.time_to_str_s(self.time))

        return result
