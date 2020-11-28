#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: buy_nongyeyinhang_strategy.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-08 09:53
# @ModifyDate: 2017-04-08 09:53
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
import time
from .base_strategy import BaseStrategy
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from quotation.quotation import Quotation
from trader.trader import Trader
from utils.date_time import get_exchange_time
from utils.tool import estimate_to_close
from utils.tool import get_turnover_brokerage
import copy

class BuyNongyeyinhangStrategy(BaseStrategy):
    """
    * 农业银行价格波动比较小，风险较低
    * 主要赚波动的钱
    * 农业银行在 买入价格 跟卖出价格 1分钱内 上下波动， 在买入价格买进，有一定概率收在卖出价格
    * 农业银行走势比较随大盘，可以以沪港通资金作为买入指标
    * 沪港通  > 2 可以买入
    * 沪港通 10点之后 当天预计 > 6, 买入
    * 10点之后参考沪港通预估值，10点之前预估波动太大
    """
    HGT_LIM = 2
    HGT_ESTIMATE_LIM = 6

    def __init__(self):
        return

    def execute(self, job):
        q = Quotation()
        hgt = q.get_hgt_capital()
        hgt_estimate = estimate_to_close(hgt)

        #沪港通指标
        buy = 0
        if hgt > self.HGT_LIM:
            buy = 1
        if get_exchange_time() > 30 * 60 and hgt_estimate > self.HGT_ESTIMATE_LIM:
            buy = 1

        if buy == 0:
            job.status = 0
            job.result.clear()
            return 0

        if buy == 1:
            job.status = 1

        t = Trader.get_instance(job['trader'])
        position = t.position()
        balance = t.balance()
        enable_balance = balance[0].enable_balance

        codes = []
        for i,v in enumerate(job.result):
            codes.append(v.code)
        quotes = q.get_realtime_quotes(codes)

        temp_result = copy.copy(job.result)
        job.result.clear()
        for i,v in enumerate(temp_result):
            #找到该股的持仓数据
            v_position = ''
            for p in position:
                if p.stock_code == v.code:
                    v_position = p
            #达到持仓上限
            if v_position != '' and v_position.current_amount >= v.amount:
                continue
            #设置买入参数
            v.price = quotes[v.code].buy
            if get_turnover_brokerage(v.price * v.amount) > enable_balance:
                continue
            enable_balance -= get_turnover_brokerage(v.price * v.amount)
            job.result.append(v)

        return 0

def main(argv):
    from .job import Job
    conf = {'name':'nongyeyinhang', 'switch':1, 'trader':'yh', 'portfolio': 'nongyeyinhang.yaml'}
    job = Job(conf)
    strategy = BuyNongyeyinhangStrategy()
    strategy.execute(job)
    print((job.status))
    print((job.result.__str__().encode('utf-8')))

if __name__ == "__main__":
    main(sys.argv)
