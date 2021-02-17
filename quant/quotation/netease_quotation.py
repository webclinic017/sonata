#!/usr/bin/python
#-*- coding: utf-8 -*- 

import sys
import os
import re
import xlrd
from .ticks import Ticks
from .base_quotation import BaseQuotation
from .quote import Quote
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.date_time as date_time
from utils.symbol import symbol_of
from utils.symbol import ne_symbol_of

class NeteaseQuotation(BaseQuotation):
    """网易免费行情获取"""
    tick_data_api = 'http://quotes.money.163.com/cjmx/%s/%s/%s.xls'

    def __init__(self):
        self.encoding = ''
        self.ticks = Ticks()

    def get_today_ticks(self, code):
        """
        获取当天tick数据
        TODO
        """
        url = self._gen_today_ticks_url(code)
        lines = self._request(url)
        return self.format_today_ticks(lines)


    def format_tick_data(self, today_ticks_data):
        """
        处理历史tick返回数据
        """
        xls = xlrd.open_workbook(file_contents=today_ticks_data)
        #xls = xlrd.open_workbook('/home/users/zhangyunsheng/sonata/quant/quotation/0600000.xls')
        table = xls.sheets()[0]
        return table.row_values(1)

    def _gen_tick_data_url(self, code, date):
        """
        生成历史tick数据获取链接
        http://quotes.money.163.com/cjmx/2016/20160520/0600000.xls
        """
        date = date_time.str_to_date(date)
        y = date_time.date_to_str(date, '%Y')
        d = date_time.date_to_str(date, '%Y%m%d')
        symbol = ne_symbol_of(code)
        if '' == symbol:
            return ''
        return self.tick_data_api % (y, d, symbol)


def main(argv):
    q = NeteaseQuotation()
    #print((q._gen_tick_data_url('sh', '2016-05-20')))
    #print((q._gen_tick_data_url('000001', '2016-05-20')))
    #print((q.get_tick_data('sh', '2016-05-20')))
    #print((q.get_today_ticks('000001')))
    #print((q.get_today_ticks('sh')))
    #print((q.get_tick_data('000001', '2020-12-01')))
    #print((q.get_tick_data('sh', '2020-12-01')))

if __name__ == "__main__":
    main(sys.argv)
