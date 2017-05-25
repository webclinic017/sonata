#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: sell_repos_strategy.py
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
from utils.date_time import get_today_time
from utils.tool import estimate_to_close

class BuyNongyeyinhangStrategy(BaseStrategy):
    """
    * 农业银行价格波动比较小，风险较低
    * 农业银行在 买入价格 跟卖出价格 1分钱内 上下波动， 在买入价格买进，有一定概率收在卖出价格
    * 农业银行走势比较随大盘，可以以沪港通资金作为买入指标
    * 沪港通  > 2.5 买入
    * 沪港通 当天预计 > 6, 买入
    * 10点之后参考沪港通预估值，10点之前预估波动太大
    """

    def __init__(self):
        return

    def execute(self, job):
        q = Quotation()
        hgt = q.get_hgt_capital()
        hgt_estimate = estimate_to_close(hgt)
        print hgt
        print hgt_estimate

        #t = Trader.get_instance(job['trader'])
        #balance = t.balance()
        #enable_balance = balance[0].enable_balance

        #q = Quotation()
        #quote = q.get_realtime_quotes([self.GC001, self.R001])
        #for (k,v) in quote.items():
        #    string = v.__str__()
        #    print string.encode('utf-8')

        #if quote[self.GC001].buy > quote[self.R001].buy and enable_balance >= self.GC001_UNIT * self.HAND:
        #    amount=int(enable_balance/self.HAND/self.GC001_UNIT)*self.GC001_UNIT
        #    ret = t.sell(self.GC001, price=quote[self.GC001].buy, amount=int(enable_balance/self.HAND/self.GC001_UNIT)*self.GC001_UNIT)
        #    job.notice(str(ret))
        #    job.trade(str(ret))

        ##不要过于频繁操作
        #time.sleep(2)
        #balance = t.balance()
        #enable_balance = balance[0].enable_balance
        #quote = q.get_realtime_quotes([self.GC001, self.R001])
        #amount=int(enable_balance/self.HAND/self.R001_UNIT)*self.R001_UNIT
        #ret = t.sell(self.R001, price=quote[self.R001].buy, amount=amount)

        #job.notice(str(ret))
        #job.trade(str(ret))

        return 0

def main(argv):
    from job import Job
    conf = {'name':'all repos', 'switch':1, 'trader':'yh', 'portfolio': 'repos.yaml'}
    job = Job(conf)
    strategy = BuyNongyeyinhangStrategy()
    strategy.execute(job)

if __name__ == "__main__":
    main(sys.argv)
