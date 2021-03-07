#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: sinaquotation.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-27 19:37
# @ModifyDate: 2016-04-27 19:37
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
import re
from .base_quotation import BaseQuotation
from .quote import Quote
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.date_time as date_time
from utils.symbol import code_from_symbol

class SinaQuotation(BaseQuotation):
    """新浪免费行情获取"""
    realtime_max = 800
    realtime_quotes_format = re.compile(r'(sh\d+|sz\d+)=([^\s][^,]+?)%s%s' % (r',([\.\d]+)' * 29, r',([-\.\d:]+)' * 2))
    realtime_quotes_api = 'http://hq.sinajs.cn/?format=text&list='
    #http://vip.stock.finance.sina.com.cn/quotes_service/view/vML_DataList.php?num=500&symbol=sz300024

    def format_realtime_quotes(self, realtime_quotes_data):
        result = dict()
        stocks_detail = ''.join(realtime_quotes_data)
        grep_result = self.realtime_quotes_format.finditer(stocks_detail)
        for stock_match_object in grep_result:
            stock = stock_match_object.groups()
            q = Quote()
            q.symbol = stock[0]
            q.code = code_from_symbol(stock[0])
            q.name = stock[1]
            q.open = float(stock[2])
            q.close = float(stock[3])
            q.now = float(stock[4])
            q.high = float(stock[5])
            q.low = float(stock[6])
            q.buy = float(stock[7])
            q.sell = float(stock[8])
            q.volume = int(stock[9])
            q.turnover = float(stock[10])
            q.bid1_volume = int(stock[11])
            q.bid1 = float(stock[12])
            q.bid2_volume = int(stock[13])
            q.bid2 = float(stock[14])
            q.bid3_volume = int(stock[15])
            q.bid3 = float(stock[16])
            q.bid4_volume = int(stock[17])
            q.bid4 = float(stock[18])
            q.bid5_volume = int(stock[19])
            q.bid5 = float(stock[20])
            q.ask1_volume = int(stock[21])
            q.ask1 = float(stock[22])
            q.ask2_volume = int(stock[23])
            q.ask2 = float(stock[24])
            q.ask3_volume = int(stock[25])
            q.ask3 = float(stock[26])
            q.ask4_volume = int(stock[27])
            q.ask4 = float(stock[28])
            q.ask5_volume = int(stock[29])
            q.ask5 = float(stock[30])
            #q.date = date_time.str_to_date(stock[31])
            q.time = date_time.str_to_time(stock[31] + ' ' + stock[32])

            result[q.code] = q

        return result


def main(argv):
    q = SinaQuotation()
    #r = q.get_realtime_quotes(['sh', '000001', '000006'])
    #r = q.get_realtime_quotes(['sh'])
    r = q.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb', 'zx300', 'zh500'])
    for (k,v) in list(r.items()):
        print(k)
        string = v.__str__
        print((string.encode('utf-8')))


if __name__ == "__main__":
    main(sys.argv)
