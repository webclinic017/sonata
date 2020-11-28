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
from .date_time import get_exchange_time


def estimate_to_close(value):
    """
    估算到收盘的值
    """

    return value * (4 * 60 * 60) / get_exchange_time()

def net_deduct_trading_fees(balance):
    """
    扣除买入手续费得到的净可用于买股票资金
    银河佣金全包 万1.8, 最低5元
    没有印花税,印花税 卖出时收 1‰
    """
    #STAMP_TAX = 1.0/1000
    BROKERAGE = 1.8/10000
    BROKERAGE_LEAST = 5
    if balance * BROKERAGE < BROKERAGE_LEAST:
        net = balance - BROKERAGE_LEAST
    else:
        net = balance/(1 + BROKERAGE)

    return net

def get_brokerage_fees(turnover):
    """
    由成交金额得到佣金金额
    银河佣金全包 万1.8, 最低5元
    """
    brokerage_fees = 5
    BROKERAGE = 1.8/10000
    BROKERAGE_LEAST = 5
    if turnover * BROKERAGE < BROKERAGE_LEAST:
        brokerage_fees = BROKERAGE_LEAST
    else:
        brokerage_fees = turnover * BROKERAGE

    return brokerage_fees

def get_turnover_brokerage(turnover):
    """
    由成交金额得到总资金，包含佣金金额
    银河佣金全包 万1.8, 最低5元
    """

    return turnover + get_brokerage_fees(turnover)

def get_value_by_key(data, key, default = ''):
    value = default
    if key in data:
        value = data[key]
    return value

def main(argv):
    print((estimate_to_close(0.89)))
    print((net_deduct_trading_fees(30000)))
    data = {'abc': 123, 'cd': 'aaa'}
    print((get_value_by_key(data, 'abc', 'default')))
    print((get_value_by_key(data, 'bbb', 'default')))
    #print get_total_balance(30000)

if __name__ == "__main__":
    main(sys.argv)
