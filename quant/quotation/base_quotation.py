#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: basequotation.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-27 16:47
# @ModifyDate: 2016-04-27 16:47
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from utils.symbol import symbol_of

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

class BaseQuotation:
    """行情获取基类"""
    encoding = 'GBK'
    realtime_max = 1
    realtime_quotes_api = 'http://hq.sinajs.cn/?format=text&list='
    today_ticks_api = ''

    def __init__(self):
        return

    def get_realtime_quotes(self, codes):
        """
        获取当前行情
        """
        if type(codes) is not list:
            codes = [codes]
        url = self._gen_realtime_quotes_url(codes)
        #request = Request(url)
        #lines = urlopen(request, timeout=10).read()
        #lines = lines.decode('GBK')
        lines = self._request(url)
        #print lines.encode('utf-8')
        return self.format_realtime_quotes(lines)

    def format_realtime_quotes(self, realtime_quotes_data):
        """
        处理实时行情返回数据
        """
        return realtime_quotes_data

    def _gen_realtime_quotes_url(self, codes):
        """
        生成行情获取链接
        """
        if len(codes) > self.realtime_max:
            return ''
        url = self.realtime_quotes_api
        for code in codes:
            symbol = self._code_to_symbol(code)
            url += symbol + ','
        return url

    def get_today_ticks(self, code):
        """
        获取当天tick数据
        """
        url = self._gen_today_ticks_url(code)
        lines = self._request(url)
        return self.format_today_ticks(lines)

    def format_today_ticks(self, today_ticks_data):
        """
        处理today ticks返回数据
        """
        return today_ticks_data

    def _gen_today_ticks_url(self, code, page=1):
        """
        生成tick数据获取链接
        """
        return code

    def get_tick_data(self, code, date):
        """
        获取历史tick数据
        """
        url = self._gen_tick_data_url(code, date)
        lines = self._request(url)
        return self.format_tick_data(lines)

    def format_tick_data(self, today_ticks_data):
        """
        处理历史tick返回数据
        """
        return today_ticks_data


    def _gen_tick_data_url(self, code, date):
        """
        生成历史tick数据获取链接
        """
        return code


    def _code_to_symbol(self, code):
        return symbol_of(code)

    def _request(self, url, retry_count=3, pause=0.001):
        for _ in range(retry_count):
            try:
                request = Request(url)
                lines = urlopen(request, timeout=10).read()
                if '' != self.encoding:
                    lines = lines.decode(self.encoding)
            except Exception as e:
                print (str(e))
            else:
                return lines
        raise IOError('network url error, url:%s' % (url))

def main(argv):
    q = BaseQuotation()
    #print q._gen_quotation_url(['sh', '000001'])
    q.get_realtime_quotes(['sh', '000001'])


if __name__ == "__main__":
    main(sys.argv)
