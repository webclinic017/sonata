#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: eastmoneyquotation.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-27 19:37
# @ModifyDate: 2016-04-27 19:37
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
import re
import json
from base_quotation import BaseQuotation
from quote import Quote
from ticks import Ticks
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.date_time as date_time
from utils.symbol import em_symbol_of
from utils.symbol import symbol_of
from utils.symbol import code_from_em_symbol

class EastmoneyQuotation(BaseQuotation):
    """东方财富免费行情获取"""
    encoding = 'utf-8'
    realtime_max = 1
    realtime_quotes_api = 'http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/CompatiblePage.aspx?Type=fs&jsName=js&Reference=xml&stk=%s'
    realtime_quotes_format = re.compile(r'var js=\{skif:"(.+)",bsif:(\[.+\]),dtif:(\[.+\]),dpif:(\[.+\])\}')
    today_ticks_api = 'http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/CompatiblePage.aspx?Type=OB&Reference=xml&limit=0&stk=%s&page=%d'
    today_ticks_format = re.compile(r'var jsTimeSharingData={pages:(\d+),data:(\[.+\])}')
    hsgt_api = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=P.(x),(x)|0000011|0000011&sty=SHSTDTA|SZSTDTA&st=z&sr=&p=&ps=&cb=&token=70f12f2f4f091e459a279469fe49eca5&js=var%20tSgkmQ=({data:[(x)]})'
    hsgt_format = re.compile(r'data:\[\"(.+)\",\"(.+)\"\]')

    def __init__(self):
        self.ticks = Ticks()

    def format_realtime_quotes(self, realtime_quotes_data):
        result = dict()
        stocks_detail = ''.join(realtime_quotes_data)
        grep_result = self.realtime_quotes_format.finditer(stocks_detail)
        for stock_match_object in grep_result:
            q = Quote()
            groups = stock_match_object.groups()
            l = json.loads(groups[1])
            ask_bid = []
            for i in l:
                ab = re.split(r',', i)
                ask_bid.append(ab)

            s = re.split(r',', groups[0])
            q.symbol = symbol_of(s[1])
            q.code = code_from_em_symbol(s[1] + s[0])
            q.name = s[2]
            q.now = float(s[3])
            q.open = float(s[8])
            q.close = float(s[9])
            q.high = float(s[10])
            q.low = float(s[11])
            q.buy = float(ask_bid[5][0])
            q.sell = float(ask_bid[4][0])
            q.volume = int(s[17]) * 100
            q.turnover = float(s[19]) * 10000
            q.bid1_volume = int(ask_bid[5][1]) * 100
            q.bid1 = float(ask_bid[5][0])
            q.bid2_volume = int(ask_bid[6][1]) * 100
            q.bid2 = float(ask_bid[6][0])
            q.bid3_volume = int(ask_bid[7][1]) * 100
            q.bid3 = float(ask_bid[7][0])
            q.bid4_volume = int(ask_bid[8][1]) * 100
            q.bid4 = float(ask_bid[8][0])
            q.bid5_volume = int(ask_bid[9][1]) * 100
            q.bid5 = float(ask_bid[9][0])
            q.ask1_volume = int(ask_bid[4][1]) * 100
            q.ask1 = float(ask_bid[4][0])
            q.ask2_volume = int(ask_bid[3][1]) * 100
            q.ask2 = float(ask_bid[3][0])
            q.ask3_volume = int(ask_bid[2][1]) * 100
            q.ask3 = float(ask_bid[2][0])
            q.ask4_volume = int(ask_bid[1][1]) * 100
            q.ask4 = float(ask_bid[1][0])
            q.ask5_volume = int(ask_bid[0][1]) * 100
            q.ask5 = float(ask_bid[0][0])
            q.time = date_time.str_to_time(s[27])

            result[q.code] = q

        return result

    def _gen_realtime_quotes_url(self, codes):
        """
        生成行情获取链接
        http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/CompatiblePage.aspx?Type=fs&jsName=js&stk=0000052&Reference=xml
        """
        if len(codes) > self.realtime_max:
            return ''
        code = codes[0]
        symbol = em_symbol_of(code)
        return self.realtime_quotes_api % (symbol)

    def get_today_ticks(self, code):
        """
        获取当天tick数据
        """
        self.ticks = Ticks()
        self.ticks.symbol = symbol_of(code)
        pages = 16
        page = 1
        while (page <= pages):
            url = self._gen_today_ticks_url(code, page)
            lines = self._request(url)
            pages = self.format_today_ticks(lines)
            page += 1
        return self.ticks

    def format_today_ticks(self, today_ticks_data):
        """
        处理today ticks返回数据
        """
        ticks_detail = ''.join(today_ticks_data)
        grep_result = self.today_ticks_format.finditer(ticks_detail)
        for stock_match_object in grep_result:
            groups = stock_match_object.groups()
            pages = int(groups[0])
            ticks = groups[1]
            #print ticks.encode('utf-8')
            l = json.loads(ticks)
            data = []
            for tick in l:
                d = re.split(r',', tick)
                data.append(d)
            df = pd.DataFrame(data, columns = self.ticks.COLUMNS)
            self.ticks.df = pd.concat([self.ticks.df, df])

            return pages
        return 0

    def _gen_today_ticks_url(self, code, page=1):
        """
        生成tick数据获取链接
        """
        #return 'http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/CompatiblePage.aspx?Type=OB&limit=0&stk=0000012&page=0'
        symbol = em_symbol_of(code)
        if '' == symbol:
            return ''
        return self.today_ticks_api % (symbol, page)

    def get_hgt_capital(self):
        """
        得到当前沪股通资金情况
        """
        capital = 0.0
        hsgt_detail = self._request(self.hsgt_api)
        grep_result = self.hsgt_format.finditer(hsgt_detail)
        for stock_match_object in grep_result:
            groups = stock_match_object.groups()
            hgt = groups[0]
            sgt = groups[1]
            sp = re.split(r',', hgt)
            capital = sp[6]
            if capital[-2:] == u'亿元':
                capital = float(capital[:-2])

        return capital



def main(argv):
    q = EastmoneyQuotation()
    #r = q.get_realtime_quotes('sh')
    #for (k,v) in r.items():
    #    print k
    #    string = v.__str__()
    #    print string.encode('utf-8')
    #r = q.get_realtime_quotes('000001')
    #for (k,v) in r.items():
    #    print k
    #    string = v.__str__()
    #    print string.encode('utf-8')
    #r = q.get_realtime_quotes('204001')
    #for (k,v) in r.items():
    #    string = v.__str__()
    #    print string.encode('utf-8')
    #r = q.get_realtime_quotes('131810')
    #for (k,v) in r.items():
    #    print k
    #    string = v.__str__()
    #    print string.encode('utf-8')
    #d = q.get_today_ticks('sh')
    #print d.symbol
    #print d.df
    d = q.get_hgt_capital()
    print d


if __name__ == "__main__":
    main(sys.argv)
