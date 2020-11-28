#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: buy_strategy.py
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

class BuyStrategy(BaseStrategy):
    """
    买入操作
    如果股票还有委托未成交，并且委托价格不一样，撤销重新委托，如果价格一样就不操作
    """

    def __init__(self):
        return

    def execute(self, job):
        t = Trader.get_instance(job['trader'])

        entrusts = t.check_available_cancels()
        entrust_to_cancle = []
        for invest in job.result[:]:
            for e in entrusts:
                if e.iotype == 'buy' and e.stock_code == invest.code:
                    if e.entrust_price == invest.price:
                        job.result.remove(invest)
                    else:
                        entrust_to_cancle.append(e.entrust_no)

        if len(entrust_to_cancle):
            ret = t.cancel_entrusts(','.join(entrust_to_cancle))
            job.notice(str(ret))
            job.trade(str(ret))
            #不要过于频繁操作
            time.sleep(1)

        for invest in job.result:
            if invest.amount == 0:
                continue
            ret = t.buy(invest.code, invest.price, invest.amount)
            job.notice(str(ret))
            job.trade(str(ret))
            #不要过于频繁操作
            time.sleep(1)

        return 0

def main(argv):
    from .job import Job
    conf = {'name':'buy', 'switch':1, 'trader':'yh', 'portfolio': 'portfolio_template.yaml'}
    job = Job(conf)
    strategy = BuyStrategy()
    strategy.execute(job)
    print((job.result.__str__().encode('utf-8')))

if __name__ == "__main__":
    main(sys.argv)
