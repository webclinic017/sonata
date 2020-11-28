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
from .base_quotation import BaseQuotation
from .quote import Quote
from .ticks import Ticks
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT
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
    #hsgt_top_api = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTCJB&token=70f12f2f4f091e459a279469fe49eca5&sty=HGT&filter=(DetailDate=^2017-04-11^)(MarketType=1)&js=var%20amRIvPQq={%22data%22:(x),%22pages%22:(tp)}&ps=10&p=1&sr=1&st=Rank&rt=49882594'
    hsgt_top_api = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTCJB&token=70f12f2f4f091e459a279469fe49eca5&sty=%s&filter=(DetailDate=^%s^)(MarketType=%d)&js=var%%20amRIvPQq={%%22data%%22:(x),%%22pages%%22:(tp)}&ps=10&p=1&sr=1&st=Rank&rt=49882594'
    #hsgt_top_api = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTCJB&token=70f12f2f4f091e459a279469fe49eca5&sty=HGT&filter=(DetailDate=^2016-06-01^)(MarketType=1)&ps=10&p=1&sr=1&st=Rank&rt=49888784'
    hsgt_top_format = re.compile(r'\"data\":(\[.+\]),\"\pages":1')
    #hsgt_his_api = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTHIS&token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType=%d)&js=var%%20FDehqpDw={%%22data%22:(x),%22pages%22:(tp)}&ps=%d&p=1&sr=-1&st=DetailDate&rt=49883996'
    #hsgt_his_api = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTHIS&token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType=1)&ps=5&p=1&sr=-1&st=DetailDate&rt=49883996'
    hsgt_his_api = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTHIS&token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType=%d)&ps=%d&p=1&sr=-1&st=DetailDate&rt=49883996'

    hsgt_his_format = re.compile(r'\"data\":(\[.+\]),\"\pages":')


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
            if capital[-2:] == '亿元':
                capital = float(capital[:-2])
            elif capital[-2:] == '万元':
                capital = float(capital[:-2])/10000

        return capital

    def get_hsgt_top(self, date_str, expire = 60*24*30):
        """
        得到沪股通、深股通 十大成交股
        """
        if not os.path.exists(CT.HSGT_DIR):
            os.makedirs(CT.HSGT_DIR)

        file_path = CT.HSGT_DIR + date_str
        expired = date_time.check_file_expired(file_path, expire)
        if expired or not os.path.exists(file_path):
            hgt_top_detail = self._request(self.hsgt_top_api % ('HGT', date_str, 1))
            hgt_grep_result = self.hsgt_top_format.finditer(hgt_top_detail)
            hgt_top_result = []
            for stock_match_object in hgt_grep_result:
                groups = stock_match_object.groups()
                hgt_top_result = json.loads(groups[0])

            sgt_top_result = []
            sgt_top_detail = self._request(self.hsgt_top_api % ('SGT', date_str, 3))
            sgt_grep_result = self.hsgt_top_format.finditer(sgt_top_detail)
            for stock_match_object in sgt_grep_result:
                groups = stock_match_object.groups()
                sgt_top_result = json.loads(groups[0])

            code = []
            name = []
            change = []
            jme = []
            mrje = []
            mcje = []
            cjje = []
            ratio = []
            market = []

            if hgt_top_result:
                for v in hgt_top_result:
                    code.append(v['Code'])
                    name.append(v['Name'].encode('utf-8'))
                    change.append(v['ChangePercent'])
                    if v['HGTJME'] == '-':
                        v['HGTJME'] = 0
                    if v['HGTMRJE'] == '-':
                        v['HGTMRJE'] = 0
                    if v['HGTMCJE'] == '-':
                        v['HGTMCJE'] = 0
                    if v['HGTCJJE'] == '-':
                        v['HGTCJJE'] = 0.1/(2^64 -1)
                    jme.append(v['HGTJME'])
                    mrje.append(v['HGTMRJE'])
                    mcje.append(v['HGTMCJE'])
                    cjje.append(v['HGTCJJE'])
                    ratio.append(v['HGTMRJE']/v['HGTCJJE'])
                    market.append(1)

            if sgt_top_result:
                for v in sgt_top_result:
                    code.append(v['Code'])
                    name.append(v['Name'].encode('utf-8'))
                    change.append(v['ChangePercent'])
                    jme.append(v['SGTJME'])
                    mrje.append(v['SGTMRJE'])
                    mcje.append(v['SGTMCJE'])
                    cjje.append(v['SGTCJJE'])
                    ratio.append(v['SGTMRJE']/v['SGTCJJE'])
                    market.append(3)

            data = {'code':code, 'name':name, 'change':change, 'jme':jme, 'mrje':mrje, 'mcje':mcje, 'cjje':cjje, 'ratio':ratio, 'market':market}
            #d = pd.DataFrame(data, index=code, columns=['name', 'jme', 'mrje', 'mcje', 'cjje', 'market'])
            d = pd.DataFrame(data, columns=['code','name', 'change', 'jme', 'mrje', 'mcje', 'cjje', 'ratio', 'market'])

            #d.to_csv(file_path, sep='\t')
            d.to_csv(file_path, sep='\t', index=False)

        if not os.path.exists(file_path):
            return pd.DataFrame()
        #d = pd.read_csv(file_path, sep='\t', index_col=0)
        d = pd.read_csv(file_path, sep='\t', index_col='code')
        code = []
        for c in d.index:
            code.append("{:0>6d}".format(c))
        name = list(d['name'])
        change = list(d['change'])
        jme = list(d['jme'])
        mrje = list(d['mrje'])
        mcje = list(d['mcje'])
        cjje = list(d['cjje'])
        ratio= list(d['ratio'])
        market = list(d['market'])
        data = {'code':code, 'name':name, 'change':change, 'jme':jme, 'mrje':mrje, 'mcje':mcje, 'cjje':cjje, 'ratio':ratio, 'market':market}
        d = pd.DataFrame(data, index = code, columns=['code', 'name', 'change', 'jme', 'mrje', 'mcje', 'cjje', 'ratio', 'market'])

        return d

    def get_hsgt_his(self, days=30, market_type=1, expire = 60*6):
        """
        得到沪股通、深股通 历史资金数据
        资金单位百万
        """
        if not os.path.exists(CT.HSGT_DIR):
            os.makedirs(CT.HSGT_DIR)

        file_path = CT.HSGT_DIR + 'hsgt_his_%d_%d' % (days, market_type)
        expired = date_time.check_file_expired(file_path, expire)
        if expired or not os.path.exists(file_path):
            hsgt_his_detail = self._request(self.hsgt_his_api % (market_type, days))
            hsgt_his_result = json.loads(hsgt_his_detail)
            date = []
            zjlr = []
            jme = []
            mrcje = []
            mccje = []
            for v in hsgt_his_result:
                date.append(v['DetailDate'][:10])
                zjlr.append(v['DRZJLR'])
                jme.append(v['DRCJJME'])
                mrcje.append(v['MRCJE'])
                mccje.append(v['MCCJE'])

            data = {'date':date, 'zjlr':zjlr, 'jme':jme, 'mrcje':mrcje, 'mccje':mccje}
            d = pd.DataFrame(data, columns=['date', 'zjlr', 'jme', 'mrcje', 'mccje'])
            d.to_csv(file_path, sep='\t', index=False)

        if not os.path.exists(file_path):
            return None
        d = pd.read_csv(file_path, sep='\t', index_col='date')

        return d


def main(argv):
    q = EastmoneyQuotation()
    r = q.get_realtime_quotes('sh')
    for (k,v) in list(r.items()):
        print(k)
        string = v.__str__()
        print((string.encode('utf-8')))
    r = q.get_realtime_quotes('000001')
    for (k,v) in list(r.items()):
        print(k)
        string = v.__str__()
        print((string.encode('utf-8')))
    r = q.get_realtime_quotes('204001')
    for (k,v) in list(r.items()):
        string = v.__str__()
        print((string.encode('utf-8')))
    r = q.get_realtime_quotes('131810')
    for (k,v) in list(r.items()):
        print(k)
        string = v.__str__()
        print((string.encode('utf-8')))
    d = q.get_today_ticks('sh')
    print((d.symbol))
    print((d.df))
    d = q.get_hgt_capital()
    print(d)
    d = q.get_hsgt_top('2016-06-01', 0)
    print(d)
    d = q.get_hsgt_his()
    print(d)


if __name__ == "__main__":
    main(sys.argv)
