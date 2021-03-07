#!/usr/bin/python
# -*- coding: utf-8 -*-
# ****************************************************************#
# @Brief: sell_repos_strategy.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-08 09:53
# @ModifyDate: 2017-04-08 09:53
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
# ***************************************************************#

import sys
import os
import time
from .base_strategy import BaseStrategy

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from quotation.quotation import Quotation
from .portfolio import Invest


class SellReposStrategy(BaseStrategy):
    """
    逆回购策略
    资金全部购买逆回购
    比较GC001 R-001价格，GC001价格高优先买GC001，不够10W的资金全部买R-001，R-001价格高全部买R-001
    GC003 R-003暂不考虑，周五节价日前价格都比较低，差不多是GC001 R-001的1/3
    """
    GC001 = '204001'
    R001 = '131810'
    HAND = 100
    GC001_UNIT = 1000
    R001_UNIT = 10

    def __init__(self):
        return

    def execute(self, job):
        broker = job.broker
        balance = broker.balance()
        enable_balance = balance[0].enable_balance

        q = Quotation()
        quote = q.get_realtime_quotes([self.GC001, self.R001])
        # for (k,v) in quote.items():
        #    string = v.__str__()
        #    print string.encode('utf-8')

        # job.result.invest = []
        job.result.clear()
        if quote[self.GC001].buy > quote[self.R001].buy and enable_balance >= self.GC001_UNIT * self.HAND:
            amount = int(enable_balance / self.HAND / self.GC001_UNIT) * self.GC001_UNIT
            # invest = Invest({'name':'GC001', 'code':self.GC001, 'amount':amount, 'price':quote[self.GC001].buy})
            invest = {'code': self.GC001, 'name': 'GC001', 'amount': amount, 'price': quote[self.GC001].buy, 'deal': Invest.INVEST_DEAL_SELL}
            job.result.append(invest)
            enable_balance = enable_balance - amount * self.HAND

        quote = q.get_realtime_quotes([self.GC001, self.R001])
        amount = int(enable_balance / self.HAND / self.R001_UNIT) * self.R001_UNIT
        # invest = Invest({'name':'R001', 'code':self.R001, 'amount':amount, 'price':quote[self.R001].buy})
        invest = {'code': self.R001, 'name': 'R001', 'amount': amount, 'price': quote[self.R001].buy, 'deal': Invest.INVEST_DEAL_SELL}
        job.result.append(invest)

        return True


def main(argv):
    from .job import Job
    conf = {'name': 'all repos', 'switch': 1, 'broker': 'manual', 'portfolio': 'repos.yaml'}
    job = Job(conf)
    strategy = SellReposStrategy()
    strategy.execute(job)
    print((job.result.__str__().encode('utf-8')))


if __name__ == "__main__":
    main(sys.argv)
