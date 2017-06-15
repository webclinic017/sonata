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
    参数：买入资金比例、买入资金量、沪深股通资金流入、止盈比例
    """
    #days = 630
    days = 120
    q = Quotation()
    hsgt_his = q.get_hsgt_his(days + 100, 1, 60 * 6)

    jme_statistics = {}
    jme_count = {}
    ratio_statistics = {}
    ratio_count = {}
    change_statistics = {}
    change_count = {}
    statistics = 0
    count = 0
    profit_count = {}
    stock_statistic = {}

    days = q.get_trade_date(days)
    days =  list(reversed(days))
    for i,day in enumerate(days):
        if i + 2 >= len(days):
            break
        next_day = days[i + 1]
        next_2_day = days[i + 2]

        print '\n' + next_day
        #资金流入
        zjlr = 0
        day_zjlr = day
        if day_zjlr in hsgt_his['zjlr']:
            zjlr = hsgt_his['zjlr'][day_zjlr]
            print zjlr
            #if zjlr < 0:
            #    continue
        d = q.get_hsgt_top(day, 60 * 24 * 30)
        if d.empty:
            continue

        #按资金量排名
        d = d.sort_index(by='jme', ascending=False)
        #d = d.sort_index(by='ratio', ascending=False)
        #d = d.head(1)
        for l in d.iterrows():
            #买入比例
            #if l[1]['ratio'] < 0.5:
            #    continue
            #if l[1]['jme'] < 0:
            #    continue
            price = q.get_h_data(l[1]['code'], 60 * 24 *30)
            if next_day not in price['open'] or next_2_day not in price['high']:
                continue
            buy_price = price['open'][next_day]
            #buy_price = price['high'][next_day]
            high_price = price['high'][next_2_day]
            high_profit = (high_price - buy_price)/buy_price
            close_price = price['close'][next_2_day]
            close_profit = (close_price - buy_price)/buy_price
            #止盈比例
            profit_percent = 0.02
            if high_profit > profit_percent:
                sell_price = buy_price * (1 + profit_percent)
                profit = profit_percent
            else:
                sell_price = close_price
                profit = close_profit
            sell_price = close_price
            profit = (close_price - buy_price)/buy_price

            #if profit < 0.00136:
            #    continue

            print '\n%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%f\t%f\t%f' % (l[1]['code'], l[1]['name'].encode('utf-8'), l[1]['change'], l[1]['jme'], l[1]['mrje'], l[1]['mcje'], l[1]['cjje'], l[1]['ratio'], l[1]['market'], buy_price, sell_price, profit)

            jme_key = int(l[1]['jme']/10000000)
            if jme_key > 20 or jme_key < -20:
                jme_key = int(jme_key/10) * 10

            if jme_key not in jme_statistics:
                jme_statistics[jme_key] = 0
                jme_count[jme_key] = 0

            #jme_statistics[jme_key] += profit
            if profit >= 0.00136:
                jme_statistics[jme_key] += 1
            jme_count[jme_key] += 1

            ratio_key = int(l[1]['ratio']*100)
            if ratio_key < 70:
                ratio_key = int(ratio_key/10) * 10

            if ratio_key not in ratio_statistics:
                ratio_statistics[ratio_key] = 0
                ratio_count[ratio_key] = 0

            #ratio_statistics[ratio_key] += profit
            if profit >= 0.00136:
                ratio_statistics[ratio_key] += 1
            ratio_count[ratio_key] += 1

            change_key = int(l[1]['change']*10)
            if change_key > 20 or change_key < -20:
                change_key = int(change_key/10) * 10
            if change_key not in change_statistics:
                change_statistics[change_key] = 0
                change_count[change_key] = 0
            #change_statistics['change_key'] += profit
            if profit >= 0.00136:
                change_statistics[change_key] += 1
            change_count[change_key] += 1

            profit_key = int(profit * 1000)
            if profit_key > 20 or profit_key < -20:
                profit_key = int(profit_key/10)*10
            if profit_key not in profit_count:
                profit_count[profit_key] = 0
            profit_count[profit_key] += 1

            stock_key = l[1]['name']
            if stock_key not in stock_statistics:
                stock_statistics[stock_key] = []

            statistics += profit
            count += 1
            # 只取第一个
            #break

    print '\njme:\n'
    keys = jme_statistics.keys()
    keys.sort()
    for k in keys:
        print str(k) + '\t' + str(jme_count[k]) + '\t' + str(float(jme_statistics[k])/jme_count[k])

    print '\nratio:\n'
    keys = ratio_statistics.keys()
    keys.sort()
    for k in keys:
        print str(k) + '\t' + str(ratio_count[k]) + '\t' + str(float(ratio_statistics[k])/ratio_count[k])

    print '\nchange:\n'
    keys = change_statistics.keys()
    keys.sort()
    for k in keys:
        print str(k) + '\t' + str(change_count[k]) + '\t' + str(float(change_statistics[k])/change_count[k])

    print '\n================='
    win = 0
    for k,v in profit_count.items():
        if k >= 1:
            win = win + v
    print '\ncount:'
    print count
    print '\nwin:'
    print float(win)/count
    print '\naverage:'
    print statistics/count
    print '\ntotal:'
    print statistics
    print '\n================='
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
