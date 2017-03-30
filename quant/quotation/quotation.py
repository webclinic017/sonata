#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: quotation.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-05-20 16:05
# @ModifyDate: 2016-05-20 16:05
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
from eastmoneyquotation import EastmoneyQuotation
from sohuquotation import SohuQuotation
from sinaquotation import SinaQuotation
from tencentquotation import TencentQuotation
from tusharequotation import TushareQuotation

class Quotation:
    """ 行情类 """

    def __init__(self):
        self.eastmoney = EastmoneyQuotation()
        self.sohu = SohuQuotation()
        self.sina = SinaQuotation()
        self.tecent = TencentQuotation()
        self.tushare = TushareQuotation()
        return

    def get_realtime_quotes(self, codes):
        """
        获取当前行情
        """
        d = self.sina.get_realtime_quotes(codes)
        return d

    def get_one_realtime_quotes(self, code):
        """
        获取当前行情
        """
        d = self.eastmoney.get_realtime_quotes(code)
        return d

    def get_today_ticks(self, code):
        """
        获取当天tick数据
        """
        d = self.eastmoney.get_today_ticks(code)
        return d

    def get_stock_basics(self, expire=60*24):
        """
        获取沪深上市公司基本情况
        :param expire: 本地数据失效时间(分)，超过时间更新本地数据,强制更新传0
        """
        d = self.tushare.get_stock_basics(expire)
        return d


    def get_h_data(self, symbol, expire=60):
        """
        获取一支股票所有历史数据保存到本地
        """
        d = self.tushare.get_h_data(symbol, expire)
        return d

    def get_tick_data(self, symbol, date, expire=60*24*365*10):
        """
        获取一支股票一天的tick数据保存到本地
        --------
        symbol: string,股票代码
        date: string,1900-01-01
        """
        d = self.tushare.get_tick_data(symbol, date, expire)
        return d



def main(argv):
    q = Quotation()
    #r = q.get_realtime_quotes('sh')
    #for (k,v) in r.items():
    #    string = v.__str__()
    #    print string.encode('utf-8')
    #d = q.get_today_ticks('sh')
    #print d.symbol
    #print d.df
    #d = q.get_h_data('000001')
    #print d
    #d = q.get_stock_basics()
    #print d
    d = q.get_tick_data('000001', '2016-05-20')
    print d

    return

if __name__ == "__main__":
    main(sys.argv)
