#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: /home/users/zhangyunsheng/sonata/quant/analysis.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-22 00:22
# @ModifyDate: 2017-04-22 00:22
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from quotation.quotation import Quotation
import tushare as ts


def dd_analysis():
    t = Quotation()
    code = '600066'

    d = t.get_h_data(code)
    d.to_csv('tt.csv', sep='\t')
    date_set = d.index[0:20]

    for date in date_set:
        buy = 0
        sell = 0
        total = 0

        d = t.get_sina_dd(code, date=date, vol=1)
        for i in d.index:
            total += d['volume'][i]
        print date + '\t' + str(total/len(d))

        #d = t.get_sina_dd(code, date=date, vol=600)
        #if d is None:
        #    continue
        ##d.to_csv('tt.csv', sep='\t')
        #for i in d.index:
        #    total += d['volume'][i]
        #    if d['type'][i].decode('utf-8') == u'买盘':
        #        buy += d['volume'][i]
        #    if d['type'][i].decode('utf-8') == u'卖盘':
        #        sell += d['volume'][i]
        #print 'buy: ' + str(buy)
        #print 'sell: ' + str(sell)
        ##print 'arerage: ' + str(total/len(d))
        ##print date + '\t' + str(total/len(d))
    return

def main(argv):
    reload(sys)
    sys.setdefaultencoding( "utf-8" )
    #dd_analysis()

    #d = ts.get_cashflow_data(2017,3)
    #d.to_csv('tt.csv', sep='\t')

    d = ts.sh_margins(start='2016-01-01', end='2017-04-22')
    print d
    d.to_csv('tt.csv', sep='\t')

    #d = ts.xsg_data()
    #d.to_csv('tt.csv', sep='\t')

    #d = ts.fund_holdings(2017, 1)
    #print d['amount']
    #d.to_csv('tt.csv', sep='\t')

    #d = ts.get_area_classified()
    #d.to_csv('tt.csv', sep='\t')

    #d = ts.get_report_data(2017,1)
    #d.to_csv('tt.csv', sep='\t')

    #d = ts.get_money_supply()
    #d.to_csv('tt.csv', sep='\t')

    #d = ts.get_cpi()
    #d.to_csv('tt.csv', sep='\t')


    #d =  ts.realtime_boxoffice()
    #d.to_csv('tt.csv', sep='\t')

    return

if __name__ == "__main__":
    main(sys.argv)
