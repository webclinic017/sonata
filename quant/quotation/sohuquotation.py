#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: sohuquotation.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-27 19:37
# @ModifyDate: 2016-04-27 19:37
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#
import sys
import os
import re
import json
from basequotation import BaseQuotation
from quote import Quote
from ticks import Ticks
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.date_time as date_time
from utils.symbol import em_symbol_of
from utils.symbol import symbol_of
from utils.symbol import zs_symbol_of
from utils.symbol import code_of


class SohuQuotation(BaseQuotation):
    """搜狐免费行情获取"""
    encoding = 'GBK'
    realtime_max = 1
    realtime_quotes_api = 'http://hq.stock.sohu.com/%s/%s/%s_%s-1.html'
    realtime_quotes_format = re.compile(r'\'price_A1\':(\[.+\]),\'price_A2\':(\[.+\]),\'perform\':(\[.+\]),\'dealdetail\'.+,\'time\':(\[.+\]),\'news_m_r\'')
    realtime_quotes_format_zs = re.compile(r'\'price_A1\':(\[.+\]),\'price_A2\':(\[.+\]),\'contribute_up\'.+,\'time\':(\[.+\])')
    today_ticks_api = 'http://hq.stock.sohu.com/%s/%s/%s_%s-3%s.html'
    today_ticks_format = re.compile(r'PEAK_ODIA\=parent\.PEAK_ODIA;\</script\>\<script\>PEAK_ODIA\((.+?)\)')

    def __init__(self):
        self.ticks = Ticks()

    def format_realtime_quotes(self, realtime_quotes_data):
        result = dict()
        stocks_detail = ''.join(realtime_quotes_data)
        grep_result = self.realtime_quotes_format_zs.finditer(stocks_detail)
        for stock_match_object in grep_result:
            groups = stock_match_object.groups()
            price_A1 = eval(groups[0])
            price_A2 = eval(groups[1])
            perform = eval('[\'\'%s]' % (',\'0\'' * 26))
            g = eval(groups[2])
        grep_result = self.realtime_quotes_format.finditer(stocks_detail)
        for stock_match_object in grep_result:
            groups = stock_match_object.groups()
            price_A1 = eval(groups[0])
            price_A2 = eval(groups[1])
            perform = eval(groups[2])
            g = eval(groups[3])

        q = Quote()
        if 'zs' == price_A1[0][:2]:
            q.symbol = zs_symbol_of(price_A1[0][-6:])
        if 'cn' == price_A1[0][:2]:
            q.symbol = symbol_of(price_A1[0][-6:])
        q.name = price_A1[1].decode('utf-8')
        q.now = float(price_A1[2])
        q.open = float(price_A2[3])
        q.close = float(price_A2[1])
        q.high = float(price_A2[5])
        q.low = float(price_A2[7])
        q.buy = float(perform[12])
        q.sell = float(perform[10])
        q.volume = int(price_A2[8]) * 100
        q.turnover = float(price_A2[12]) * 10000
        q.bid1_volume = int(perform[13]) * 100
        q.bid1 = float(perform[12])
        q.bid2_volume = int(perform[15]) * 100
        q.bid2 = float(perform[14])
        q.bid3_volume = int(perform[17]) * 100
        q.bid3 = float(perform[16])
        q.bid4_volume = int(perform[19]) * 100
        q.bid4 = float(perform[18])
        q.bid5_volume = int(perform[21]) * 100
        q.bid5 = float(perform[20])
        q.ask1_volume = int(perform[11]) * 100
        q.ask1 = float(perform[10])
        q.ask2_volume = int(perform[9]) * 100
        q.ask2 = float(perform[8])
        q.ask3_volume = int(perform[7]) * 100
        q.ask3 = float(perform[6])
        q.ask4_volume = int(perform[5]) * 100
        q.ask4 = float(perform[4])
        q.ask5_volume = int(perform[3]) * 100
        q.ask5 = float(perform[2])
        t = '%s-%s-%s %s:%s:%s' % (g[0], g[1], g[2], g[3], g[4], g[5])
        q.time = date_time.str_to_time(t)

        result[q.symbol] = q

        return result

    def _gen_realtime_quotes_url(self, codes):
        """
        生成行情获取链接
        http://hq.stock.sohu.com/cn/001/cn_204001-1.html
        """
        if len(codes) > self.realtime_max:
            return ''
        code = codes[0]
        c = code_of(code)
        if '' == c:
            return ''
        if code_of(code) != code:
            #指数链接
            t = 'zs'
        else:
            #股票链接
            t = 'cn'
        g = code_of(code)[3:]
        return self.realtime_quotes_api % (t, g, t, c)


    def get_today_ticks(self, code):
        """
        获取当天tick数据
        """
        self.ticks = Ticks()
        self.ticks.symbol = symbol_of(code)
        pages = 16
        page = 1
        while (page <= pages):
            try:
                url = self._gen_today_ticks_url(code, page)
                lines = self._request(url)
                self.format_today_ticks(lines)
                page += 1
            except IOError:
                break
        url = self._gen_today_ticks_url(code, 0)
        lines = self._request(url)
        pages = self.format_today_ticks(lines)
        return self.ticks

    def format_today_ticks(self, today_ticks_data):
        """
        处理today ticks返回数据
        """
        ticks_detail = ''.join(today_ticks_data)
        grep_result = self.today_ticks_format.finditer(ticks_detail)
        for stock_match_object in grep_result:
            groups = stock_match_object.groups()
            ticks = groups[0]
            tick_format = re.compile(r'\[\'([^,\']+)\',\'([^,\']+)\',\'([^,\']+)\',\'([^,\']+)\',\'([^,\']+)\'\]')
            tick_result = tick_format.finditer(ticks)
            data = []
            for tick_object in tick_result:
                tick_groups = tick_object.groups()
                time = tick_groups[0]
                price = abs(float(tick_groups[1]))
                #change = tick_groups[2]
                volume = tick_groups[3]
                #turnover = tick_groups[4]
                t = 1 if float(tick_groups[1]) > 0 else -1
                data.append([time, price, volume, t])
            df = pd.DataFrame(data, columns = self.ticks.COLUMNS)
            self.ticks.df = pd.concat([self.ticks.df, df])
        return 0

    def _gen_today_ticks_url(self, code, page=1):
        """
        生成tick数据获取链接
        http://hq.stock.sohu.com/cn/001/cn_000001-3.html
        http://hq.stock.sohu.com/zs/001/zs_000001-3-13.html
        """
        c = code_of(code)
        if '' == c:
            return ''
        if code_of(code) != code:
            #指数链接
            t = 'zs'
        else:
            #股票链接
            t = 'cn'
        g = code_of(code)[3:]
        if 0 == page:
            p = ''
        else:
            p = '-%d' % (page)
        return self.today_ticks_api % (t, g, t, c, p)


def main(argv):
    q = SohuQuotation()
    #r = q.get_realtime_quotes('sh')
    #for (k,v) in r.items():
    #    string = v.__str__()
    #    print string.encode('utf-8')
    r = q.get_realtime_quotes('000001')
    for (k,v) in r.items():
        string = v.__str__()
        print string.encode('utf-8')
    r = q.get_realtime_quotes('204001')
    for (k,v) in r.items():
        string = v.__str__()
        print string.encode('utf-8')
    #r = q.get_realtime_quotes('131810')
    #for (k,v) in r.items():
    #    string = v.__str__()
    #    print string.encode('utf-8')
    #r = q.get_realtime_quotes('000006')
    #for (k,v) in r.items():
    #    string = v.__str__()
    #    print string.encode('utf-8')
    #d = q.get_today_ticks('sh')
    #print d.symbol
    #print d.df


if __name__ == "__main__":
    main(sys.argv)
