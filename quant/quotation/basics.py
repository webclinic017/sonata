#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: basic.py 获取所有股票基本信息保存到本地
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-18 00:11
# @ModifyDate: 2016-04-18 00:14
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import tushare as ts
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT
import utils.date_time as date_time

class Basics:
    """基本面数据"""

    def __init__(self):
        return

    def get_stock_basics(self, expire=60*24):
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
        if expired:
            d = ts.get_stock_basics()
            d = d.sort_index()
            d.to_csv(CT.BASICS_DIR + './basics.csv')

            all_stock_symbol = open(CT.BASICS_DIR + './symbols.csv', 'w')
            stock_symbol = []
            for symbol in d['name'].index:
                stock_symbol.append(symbol + '\n')
            all_stock_symbol.writelines(stock_symbol)
            all_stock_symbol.close()
            return d
        else:
            d = pd.read_csv(basics_file_path)
            return d

def main(argv):
    b = Basics()
    d = b.get_stock_basics(0)
    print d
    #d.sort_values(by='pe').to_csv(CT.BASICS_DIR + './basics_by_pe.csv')
    return

if __name__ == "__main__":
    main(sys.argv)
