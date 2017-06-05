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
import pandas as pd


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

def hsgt_top_analysis():
    """
    分析沪深股通 top成交 策略
    """
    days = 120
    q = Quotation()
    hsgt_his = q.get_hsgt_his(days + 100, 1, 60 * 24 *30)
    #d = q.get_hsgt_top('2017-06-02')
    #for l in d.iterrows():
    #    print l[1]['name'].encode('utf-8')

    jme_statistics = {}
    jme_count = {}
    ratio_statistics = {}
    ratio_count = {}
    statistics = 0
    count = 0
    profit_count = {}

    days = q.get_trade_date(days)
    days =  list(reversed(days))
    #for i,day in enumerate(list(reversed(days))):
    for i,day in enumerate(days):
        if i + 2 >= len(days):
            break
        next_day = days[i + 1]
        next_2_day = days[i + 2]

        print '\n' + next_day
        if next_day in hsgt_his['zjlr']:
            print hsgt_his['zjlr'][next_day]
            #if hsgt_his['zjlr'][next_day] < 0:
            #    continue
        d = q.get_hsgt_top(day)
        if d.empty:
            continue

        #d = d.sort_index(by='jme', ascending=False)
        #jme_code = ''
        #jme_profit = ''
        #max_jme = 0
        #ratio_code = ''
        #d = d.sort_index(by='ratio', ascending=False)
        d = d.sort_index(by='jme', ascending=False)
        #d = d.head(3)
        for l in d.iterrows():
            if l[1]['ratio'] < 0.94:
                continue
            #if l[1]['jme'] < 40000000:
            #    continue
            price = q.get_h_data(l[1]['code'])
            if next_day not in price['open'] or next_2_day not in price['high']:
                continue
            buy_price = price['open'][next_day]
            #buy_price = price['high'][next_day]
            sell_price = price['high'][next_2_day]
            profit = (sell_price - buy_price)/buy_price

            #if l[1]['jme'] > max_jme:
            #    max_jme = l[1]['jme']
            #    jme_profit = profit
            #    jem_code = l[1]['code']
            #if ratio_code == '':
            #    ratio_code = l[1]['code']
            #else:
            #    continue

            print '\n%s\t%s\t%f\t%f\t%f\t%f\t%f\t%d\t%f\t%f\t%f' % (l[1]['code'], l[1]['name'].encode('utf-8'), l[1]['jme'], l[1]['mrje'], l[1]['mcje'], l[1]['cjje'], l[1]['ratio'], l[1]['market'], buy_price, sell_price, profit)

            jme_key = int(l[1]['jme']/10000000)
            if jme_key not in jme_statistics:
                jme_statistics[jme_key] = 0
                jme_count[jme_key] = 0

            jme_statistics[jme_key] += profit
            jme_count[jme_key] += 1

            ratio_key = int(l[1]['ratio']*100)
            if ratio_key < 70:
                ratio_key = int(ratio_key/10)

            if ratio_key not in ratio_statistics:
                ratio_statistics[ratio_key] = 0
                ratio_count[ratio_key] = 0

            ratio_statistics[ratio_key] += profit
            ratio_count[ratio_key] += 1

            profit_key = int(profit * 100)
            if profit_key not in profit_count:
                profit_count[profit_key] = 0
            profit_count[profit_key] += 1

            statistics += profit
            count += 1
            break

        #if jme_code != ratio_code:
        #    profit_key = int(jme_profit * 100)
        #    if profit_key not in profit_count:
        #        profit_count[profit_key] = 0
        #    profit_count[profit_key] += 1
        #    statistics += jme_profit
        #    count += 1

    print '\njme:\n'
    keys = jme_statistics.keys()
    keys.sort()
    for k in keys:
        print str(k) + '\t' + str(jme_statistics[k]/jme_count[k])

    print '\nratio:\n'
    keys = ratio_statistics.keys()
    keys.sort()
    for k in keys:
        print str(k) + '\t' + str(ratio_statistics[k]/ratio_count[k])

    print '\ntotal:\n'
    print statistics/count
    print count
    keys = profit_count.keys()
    keys.sort()
    for k in keys:
        print str(k) + '\t' + str(profit_count[k])

    return


def main(argv):
    reload(sys)
    sys.setdefaultencoding( "utf-8" )
    #dd_analysis()

    #d = ts.get_cashflow_data(2017,3)
    #d.to_csv('tt.csv', sep='\t')

    #d = ts.sh_margins(start='2016-01-01', end='2017-04-22')
    #print d
    #d.to_csv('tt.csv', sep='\t')

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

    d = hsgt_top_analysis()

    return

if __name__ == "__main__":
    main(sys.argv)
