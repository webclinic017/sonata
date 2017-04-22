#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: get_tick.py 获取tick历史数据
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-18 00:11
# @ModifyDate: 2016-04-18 01:06
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import tushare as ts
import time
import datetime
import os
import sys
import threading
import logging
import getopt
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from quotation.quotation import Quotation
import utils.const as CT
import utils.date_time as date_time

global g_expire
g_expire = 60*24*365*10

def get_tick_data_mul(symbol, dates):
    """
    获取一支股票一个时间段的tick数据
    把日期按线程数切片分给线程处理
    """

    class TickDataThread(threading.Thread):
        """
        获取一支股票一个时间段的tick数据
        """
        def __init__(self, symbol, dates):
            threading.Thread.__init__(self)
            self.symbol = symbol
            self.dates = dates

        def run(self):
            q = Quotation()
            for date in self.dates:
                q.get_tick_data(self.symbol, date)

    sep_len = (len(dates) + CT.TICK_THRD_CNT -1)/CT.TICK_THRD_CNT
    threads = []
    for i in range(0,len(dates), sep_len):
        b = dates[i:i+sep_len]
        t = TickDataThread(symbol, b)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return True


def get_tick_data_symbol(symbol, index, thrd_cnt):
    """
    获取一支股票所有的tick数据
    """
    if not os.path.exists(CT.TICK_DIR + symbol):
        os.makedirs(CT.TICK_DIR + symbol)
    q = Quotation()
    d = q.get_his_data(symbol)
    sep_len = (len(d.index) + thrd_cnt -1)/thrd_cnt
    start = sep_len * index
    end = sep_len * (index + 1)
    dates = d.index[start:end]
    get_tick_data_mul(symbol, dates)
    return True

def get_tick_data_date(date, index, thrd_cnt):
    """
    获取一天内所有股票tick数据
    """
    symbols = open(CT.BASICS_DIR + 'symbols.csv')
    symbols_list = []
    for c in symbols:
        symbols_list.append(c.strip())

    sep_list_len = (len(symbols_list) + thrd_cnt -1)/thrd_cnt

    start = sep_list_len * index
    end = sep_list_len * (index + 1)
    sep_symbols_list = symbols_list[start:end]
    q = Quotation()
    for s in sep_symbols_list:
        q.get_tick_data(s, date)
    return True

def get_symbol_tick_data_since(symbol, date):
    """
    获取一支股票从指定日期至今所有的tick数据
    --------
    symbol: string,000001
    date: string,1900-01-01
    """
    since = date_time.str_to_date(date)
    today = datetime.datetime.today()
    days = (today - since).days
    q = Quotation()
    for delta in range(0, days + 1):
        day = date_time.compute_date(since, delta)
        q.get_tick_data(symbol, day)

    return True

def get_tick_data_since(date, index, thrd_cnt):
    """
    获取一支股票从指定日期至今所有的tick数据
    date: string,1900-01-01
    index: int,线程索引
    thrd_cnt， int，总线程数
    """
    symbols = open(CT.BASICS_DIR + 'symbols.csv')
    symbols_list = []
    for c in symbols:
        symbols_list.append(c.strip())

    sep_list_len = (len(symbols_list) + thrd_cnt -1)/thrd_cnt

    start = sep_list_len * index
    end = sep_list_len * (index + 1)
    sep_symbols_list = symbols_list[start:end]
    for s in sep_symbols_list:
        get_symbol_tick_data_since(s, date)
    return True

def help():
    print( u'''
        -d,--debug	开启debug log
        -f,--force	强制更新
        -i,--index	线程索引
        -t,--thread	总线程数
        -s,--symbol	股票代码
        -a,--date	日期 1900-01-01
        -h,--help	查看用法
        -m.--mode	mode[tick,since,symbol,date,allsince]
        --------
        取得一支股票一天的tick:
        python tick.py -m tick -s $2 -a $3
        获取一支股票从指定日期至今所有的tick数据:
        python tick.py -m since -s $2 -a $3 -i i -t HIS_THRD_CNT &
        取得一支股票所有的tick:
        python tick.py -m symbol -s $2 -i i -t HIS_THRD_CNT &
        取得一天内所有股票的tick:
        python tick.py -m date -a $2 -i i -t HIS_THRD_CNT &
        获取所有股票从指定日期至今所有的tick数据:
        python tick.py -m allsince -a $2 -i i -t HIS_THRD_CNT &
    '''.encode('utf-8'));

def main(argv):
    #get_all_tick_data('000001')
    try:
        opts, args = getopt.getopt(argv[1:], "dhe:m:i:t:s:a:")
    except getopt.GetoptError, err:
        print err
        return -1
    log_level = logging.INFO
    mode = ''
    index = 0
    thread = 1
    symbol = '000000'
    date = date_time.get_today_str()
    for ok, ov in opts:
        if ok in ('-d', '--debug'):
            log_level = logging.DEBUG
        if ok in ('-e', '--expire'):
            global g_expire
            g_expire = int(ov)
        if ok in ('-m', '--mode'):
            mode = ov
        if ok in ('-i', '--index'):
            index = int(ov)
        if ok in ('-t', '--thread'):
            thread = int(ov)
        if ok in ('-s', '--symbol'):
            symbol = ov
        if ok in ('-a', '--date'):
            date = ov
        if ok in ('-h', '--help'):
            help()
            return

    logging.basicConfig(level=log_level,
            format='%(levelname)s: %(asctime)s [%(pathname)s:%(lineno)d] %(message)s',
            datefmt='%Y-%M-%d %H:%M:%S',
            filename=CT.LOG_DIR + 'tick.log',
            filemode='a')

    log_str = 'running model[%s] index[%d] thread[%d] symbol[%s] date[%s]' %(mode, index, thread, symbol, date)
    print log_str
    logging.info(log_str)
    if mode == 'symbol':
        get_tick_data_symbol(symbol, index, thread)
    elif mode == 'date':
        get_tick_data_date(date, index, thread)
    elif mode == 'allsince':
        get_tick_data_since(date, index, thread)
    elif mode == 'since':
        get_symbol_tick_data_since(symbol, date)
    elif mode == 'tick':
        q = Quotation()
        q.get_tick_data(symbol, date)
    else:
        print('args err mode[%s]' %(mode))
        logging.error('args err mode[%s]' %(mode))
    return

if __name__ == "__main__":
    main(sys.argv)
