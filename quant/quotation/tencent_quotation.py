#!/usr/bin/python
#-*- coding: utf-8 -*- 

import sys
import os
import re
import datetime
from .base_quotation import BaseQuotation
from .quote import Quote
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.date_time as date_time
from utils.symbol import code_from_symbol

class TencentQuotation(BaseQuotation):
    """腾讯免费行情获取"""
    realtime_max = 60
    #grep_detail = re.compile(r'(sh\d+|sz\d+)=([\d]+)~([^\s][^~]+?)%s%s%s' % (r'~([\.\d]+)' * 27, r'~([\w\.:\|\/]+)', r'~([-\.\d\/]+)' * 17 ))
    realtime_quotes_format = re.compile(r'(sh\d+|sz\d+)=([^\s][\d]+)%s' % (r'~([^~]*)' * 48))
    realtime_quotes_api = 'http://qt.gtimg.cn/q='

    def format_realtime_quotes(self, realtime_quotes_data):
        result = dict()
        stocks_detail = ''.join(realtime_quotes_data)
        #stock_detail_list = stocks_detail.split(';')
        grep_result = self.realtime_quotes_format.finditer(stocks_detail)
        for stock_match_object in grep_result:
            #i = 0
            #for x in stock_match_object.groups():
            #    print i
            #    print x.encode('utf-8')
            #    i += 1
            stock = stock_match_object.groups()
            q = Quote()
            q.symbol = stock[0]
            q.code = code_from_symbol(q.symbol)
            q.name = stock[2]
            q.open = float(stock[6])
            q.close = float(stock[5])
            q.now = float(stock[4])
            q.high = float(stock[34])
            q.low = float(stock[35])
            q.buy = float(stock[10])
            q.sell = float(stock[20])
            q.turnover = float(stock[38]) * 10000
            q.volume = int(stock[37]) * 100
            q.bid1_volume = int(stock[11]) * 100
            q.bid1 = float(stock[10])
            q.bid2_volume = int(stock[13]) * 100
            q.bid2 = float(stock[12])
            q.bid3_volume = int(stock[15]) * 100
            q.bid3 = float(stock[14])
            q.bid4_volume = int(stock[17]) * 100
            q.bid4 = float(stock[16])
            q.bid5_volume = int(stock[19]) * 100
            q.bid5 = float(stock[18])
            q.ask1_volume = int(stock[21]) * 100
            q.ask1 = float(stock[20])
            q.ask2_volume = int(stock[23]) * 100
            q.ask2 = float(stock[22])
            q.ask3_volume = int(stock[25]) * 100
            q.ask3 = float(stock[24])
            q.ask4_volume = int(stock[27]) * 100
            q.ask4 = float(stock[26])
            q.ask5_volume = int(stock[29]) * 100
            q.ask5 = float(stock[28])
            #q.date = date_time.str_to_date(stock[31])
            q.time = datetime.datetime.strptime(stock[31], '%Y%m%d%H%M%S')

            result[q.code] = q

        return result


def main(argv):
    q = TencentQuotation()
    r = q.get_realtime_quotes(['sh', '000001', '000006'])
    #r = q.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])
    for (k,v) in list(r.items()):
        print(k)
        string = v.__str__()
        print((string.encode('utf-8')))


if __name__ == "__main__":
    main(sys.argv)
