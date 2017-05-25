#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: tusharequotation.py 获取天级历史数据
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-18 00:11
# @ModifyDate: 2016-04-18 00:13
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import tushare as ts
import pandas as pd
import time
import os
import sys
import logging
import getopt
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT
import utils.date_time as date_time

class TushareQuotation:
    """历史数据"""

    def __init__(self):
        return

    def get_stock_basics(self, expire=60*6):
        """
        获取沪深上市公司基本情况
        :param expire: 本地数据失效时间(分)，超过时间更新本地数据,强制更新传0

        @result:
        code,代码
        name,名称
        industry,所属行业
        area,地区
        pe,市盈率
        outstanding,流通股本
        totals,总股本(万)
        totalAssets,总资产(万)
        liquidAssets,流动资产
        fixedAssets,固定资产
        reserved,公积金
        reservedPerShare,每股公积金
        eps,每股收益
        bvps,每股净资
        pb,市净率
        timeToMarket,上市日期
        """
        if not os.path.exists(CT.BASICS_DIR):
            os.makedirs(CT.BASICS_DIR)

        basics_file_path = CT.BASICS_DIR + './basics.csv'

        expired = date_time.check_file_expired(basics_file_path, expire)
        if expired or not os.path.exists(basics_file_path):
            d = ts.get_stock_basics()
            d = d.sort_index()
            #d.to_csv(CT.BASICS_DIR + './basics.csv', sep='\t', index=True)
            d.to_csv(CT.BASICS_DIR + './basics.csv', sep='\t')

            all_stock_symbol = open(CT.BASICS_DIR + './symbols.csv', 'w')
            stock_symbol = []
            for symbol in d['name'].index:
                stock_symbol.append(symbol + '\n')
            all_stock_symbol.writelines(stock_symbol)
            all_stock_symbol.close()
            #return d

        d = pd.read_csv(basics_file_path, sep='\t', index_col=0)
        #d = pd.read_csv(basics_file_path)
        return d

    def get_h_data(self, symbol, expire=60*6):
        """
        获取一支股票所有历史数据保存到本地
        """
        if not os.path.exists(CT.HIS_DIR):
            os.makedirs(CT.HIS_DIR)
        file_path = CT.HIS_DIR + symbol
        expired = date_time.check_file_expired(file_path, expire)
        if expired or not os.path.exists(file_path):
            today = date_time.get_today_str()
            d = ts.get_h_data(symbol, autype=None, start=CT.START, end=today, drop_factor=False)
            #index = []
            #for i in list(d.index):
            #    index.append(date_time.date_to_str(i))
            #d = d.reindex(index, method='ffill')
            if d is None:
                return d
            d.to_csv(CT.HIS_DIR + symbol, sep='\t')
            #return d

        if not os.path.exists(file_path):
            return None
        d = pd.read_csv(file_path, sep='\t', index_col=0)
        return d

    def get_tick_data(self, symbol, date, expire=60*24*365*10):
        """
        获取一支股票一天的tick数据保存到本地
        --------
        symbol: string,股票代码
        date: string,1900-01-01
        """
        if not os.path.exists(CT.TICK_DIR):
            os.makedirs(CT.TICK_DIR)
        if not os.path.exists(CT.TICK_DIR +  symbol):
            os.makedirs(CT.TICK_DIR + symbol)

        file_path = CT.TICK_DIR + symbol + '/' + date
        expired = date_time.check_file_expired(file_path, expire)
        if expired or not os.path.exists(file_path):
            d = ts.get_tick_data(symbol, date)
            #过掉当天没数据的
            if d is None or len(d) < 10:
                return None
            d.to_csv(file_path, sep='\t')

        if not os.path.exists(file_path):
            return None

        d = pd.read_csv(file_path, sep='\t', index_col=1)

        #过掉当天没数据的
        if d is None or len(d) < 10:
            return None
        return d

    def get_today_shibor_ON(self):
        """
        获取今天的银行间拆借利率 隔夜(O/N)
        """
        d = ts.shibor_data() #取当前年份的数据
        #print d.sort('date', ascending=False).head(10)
        return d['ON'][len(d['ON']) - 1]

    def get_sina_dd(self, code, date='', vol=400):
        """
        大单交易数据
        """
        if date == '':
            date = date_time.get_today_str()
        d = ts.get_sina_dd(code, date=date, vol=vol)
        return d

def main(argv):
    t = TushareQuotation()

    d = t.get_stock_basics(0)
    print d.index
    print d['pe'][d.index[0]]
    print d['name']
    d.to_csv('tt.csv', sep='\t', index=True)

    #d = t.get_h_data('002337', expire=0)
    #print d.index[0]
    #print d.index
    #d.to_csv('tt.csv', sep='\t', index=True)
    #print d

    #d = t.get_tick_data('000001', '2017-04-20', expire=0)
    #print d
    #print d.index
    #d.to_csv('tt.csv', sep='\t')

    #d = t.get_today_shibor_ON()
    #print d

    #d = t.get_sina_dd('600340', date='2017-04-21', vol=400)
    #d.to_csv('tt.csv', sep='\t')
    return

if __name__ == "__main__":
    main(sys.argv)
