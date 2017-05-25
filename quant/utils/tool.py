#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: date_time.py 定义工具
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-18 00:11
# @ModifyDate: 2016-04-18 00:23
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
import datetime
import time
from date_time import get_exchange_time


def estimate_to_close(value):
    """
    估算到收盘的值
    """

    return value * (4 * 60 * 60) / get_exchange_time()

def net_deduct_trading_fees(balance):
    """
    扣除买入手续费得到的净可用于买股票资金
    印花税 1‰
    银河佣金全包 万1.8, 最低5元
    """
    # TODO 错了 印花税 卖出时收
    STAMP_TAX = 1.0/1000
    BROKERAGE = 1.8/10000
    BROKERAGE_LEAST = 5
    if balance * BROKERAGE < BROKERAGE_LEAST:
        net = (balance - BROKERAGE_LEAST)/(1 + STAMP_TAX)
    else:
        net = balance/(1 + STAMP_TAX + BROKERAGE)

    return net

def get_value_by_key(data, key, default = ''):
    value = default
    if data.has_key(key):
        value = data[key]
    return value

def main(argv):
    #print estimate_to_close(0.89)
    #print net_deduct_trading_fees(30000)
    data = {'abc':123, 'cd':'aaa'}
    print get_value_by_key(data, 'abc', 'default')
    print get_value_by_key(data, 'bbb', 'default')

if __name__ == "__main__":
    main(sys.argv)
