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

class SellReposStrategy(BaseStrategy):
    GC001 = '204001'
    R001 = '131810'
    HAND = 100
    GC001_UNIT = 1000
    R001_UNIT = 10
    """
    逆回购策略
    资金全部购买逆回购
    比较GC001 R-001价格，GC001价格高优先买GC001，不够10W的资金全部买R-001，R-001价格高全部买R-001
    GC003 R-003暂不考虑，周五节价日前价格都比较低，差不多是GC001 R-001的1/3
    """

    def __init__(self):
        return

    def execute(self, job):
        t = Trader(job['trader'])
        balance = t.balance()
        if isinstance(balance, list):
            balance = balance[0]
        enable_balance = balance[u'可用资金']

        q = Quotation()
        quote = q.get_realtime_quotes([self.GC001, self.R001])
        for (k,v) in quote.items():
            string = v.__str__()
            print string.encode('utf-8')

        if quote[self.GC001].buy > quote[self.R001].buy and enable_balance >= self.GC001_UNIT * self.HAND:
            amount=int(enable_balance/self.HAND/self.GC001_UNIT)*self.GC001_UNIT
            ret = t.sell(self.GC001, price=quote[self.GC001].buy, amount=int(enable_balance/self.HAND/self.GC001_UNIT)*self.GC001_UNIT)
            if isinstance(ret, list):
                ret = ret[0]
            trade_info = ""
            for (k,v) in ret.items():
                trade_info += k + ':' + str(v) + ', '
            job.notice(trade_info)
            job.trade(trade_info)

        quote = q.get_realtime_quotes([self.GC001, self.R001])
        amount=int(enable_balance/self.HAND/self.R001_UNIT)*self.R001_UNIT
        ret = t.sell(self.R001, price=quote[self.R001].buy, amount=amount)

        #ret = t.sell('601288', price=3.36, amount=100)


        #trade_info = '%s' % (ret)
        if isinstance(ret, list):
            ret = ret[0]
        trade_info = ""
        for (k,v) in ret.items():
            trade_info += k + ':' + str(v) + ', '
        job.notice(trade_info)
        job.trade(trade_info)

        return 0

def main(argv):
    from job import Job
    conf = {'name':'all repos', 'switch':1, 'trader':'yh', 'portfolio': 'repos.yaml'}
    job = Job(conf)
    strategy = SellReposStrategy()
    strategy.execute(job)

if __name__ == "__main__":
    main(sys.argv)
