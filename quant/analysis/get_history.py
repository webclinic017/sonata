#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: get_history.py 获取天级历史数据
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-18 00:11
# @ModifyDate: 2016-04-18 00:13
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import tushare as ts
import pandas as pd
import time
import os
import sys
import logging
import getopt
#from tushare_quotation import TushareQuotation
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from quotation.quotation import Quotation
import utils.const as CT
import utils.date_time as date_time

global g_expire
g_expire = 60

def get_h_data_mul(index, thread):
    """
    获取所有股票的历史数据
    """
    symbols = open(CT.BASICS_DIR + 'symbols.csv')
    symbols_list = []
    for c in symbols:
        symbols_list.append(c.strip())


    sep_list_len = (len(symbols_list) + thread -1)/thread

    start = sep_list_len * index
    end = sep_list_len * (index + 1)
    sep_symbols_list = symbols_list[start:end]
    #print sep_symbols_list
    for c in sep_symbols_list:
        global g_expire
        q = Quotation()
        q.get_h_data(c, g_expire)

def help():
    print(( '''
        -d,--debug	开启debug log
        -f,--force	强制更新
        -i,--index	线程索引
        -t,--thread	总线程数
        -s,--symbol	股票代码
        -a,--date	日期 1900-01-01
        -h,--help	查看用法
        -m.--mode	mode[all,symbol]
        --------
        获取所有股票的历史数据:
        python get_history.py -m all -i i -t HIS_THRD_CNT &
        获取指定股票历史数据:
        python get_history.py -m symbol -s $1
    '''.encode('utf-8')));
    return

def main(argv):
    #t = TushareQuotation()
    #d = t.get_h_data('002337')
    #print d
    #return
    try:
        opts, args = getopt.getopt(argv[1:], "dhe:m:i:t:s:a:")
    except getopt.GetoptError as err:
        print(err)
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
            filename=CT.LOG_DIR + 'get_history.log',
            filemode='a')

    log_str = 'running model[%s] index[%d] thread[%d] symbol[%s] date[%s]' %(mode, index, thread, symbol, date)
    print(log_str)
    logging.info(log_str)
    if mode == 'all':
        get_h_data_mul(index, thread)
    elif mode == 'symbol':
        q = Quotation()
        q.get_h_data(symbol, g_expire)
    else:
        print(('args err mode[%s]' %(mode)))
        logging.error('args err mode[%s]' %(mode))
    return

if __name__ == "__main__":
    main(sys.argv)
