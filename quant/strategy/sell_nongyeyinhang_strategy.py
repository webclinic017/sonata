#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: sell_nongyeyinhang_strategy.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-08 09:53
# @ModifyDate: 2017-04-08 09:53
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
import time
from base_strategy import BaseStrategy
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from quotation.quotation import Quotation
from trader.trader import Trader
from utils.date_time import get_exchange_time
from utils.tool import estimate_to_close
from utils.tool import get_turnover_brokerage
import copy

class SellNongyeyinhangStrategy(BaseStrategy):
    """
    * 沪港通 < -0.5, 价格涨3分(约0.85%)以上， 卖出
    * 沪港通 当天预计 < 2,  价格涨3分(约0.85%)以上， 卖出
    * 沪港通 < -1 ,  价格不低于买入价格， 保本卖出
    * 沪港通 当天预计 < -4, 价格不低于买入价格， 保本卖出
    """
    HGT_ESTIMATE_LIM = 2
    HGT_LIM = -0.5
    INCOME_RATION_LIM = 0.008
    HGT_KEEP_LIM = -1
    HGT_KEEP_ESTIMATE_LIM = 2

    def __init__(self):
        return

    def execute(self, job):
        q = Quotation()
        hgt = q.get_hgt_capital()
        hgt_estimate = estimate_to_close(hgt)

        #沪港通指标
        sell = 0
        if hgt < self.HGT_LIM:
            sell = 1
        if get_exchange_time() > 30 * 60 and hgt_estimate < self.HGT_ESTIMATE_LIM:
            sell = 1
        if hgt < self.HGT_KEEP_LIM:
            sell = 2
        if get_exchange_time() > 30 * 60 and hgt_estimate < self.HGT_KEEP_ESTIMATE_LIM:
            sell = 2

        if sell == 0:
            job.status = 0
            job.result.clear()
            return 0

        if sell != 0:
            job.status = 1

        t = Trader.get_instance(job['trader'])
        position = t.position()

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
            #没有持仓
            if v_position == '':
                continue
            #盈利卖出
            if sell == 1:
                v.price = max(quotes[v.code].buy, round(v_position.keep_cost_price * (1 + self.INCOME_RATION_LIM), 2))
            #保本卖出
            elif sell == 2:
                v.price = v_position.keep_cost_price

            # TODO 取消托单量
            #设置卖出参数
            v.amount = v_position.enable_amount
            job.result.append(v)

        return 0

def main(argv):
    from job import Job
    conf = {'name':'nongyeyinhang', 'switch':1, 'trader':'yh', 'portfolio': 'nongyeyinhang.yaml'}
    job = Job(conf)
    strategy = SellNongyeyinhangStrategy()
    strategy.execute(job)
    print job.status
    print job.result.__str__().encode('utf-8')

if __name__ == "__main__":
    main(sys.argv)
