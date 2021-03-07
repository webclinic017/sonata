#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
from .base_strategy import BaseStrategy
from .portfolio import Invest

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from quotation.quotation import Quotation
from broker.broker import Broker


class DealStrategy(BaseStrategy):
    """
    交易操作
    根据Invest的交易类型执行 买入、卖出 操作
    """

    def __init__(self):
        super().__init__()
        self.broker = None
        self.job = None
        return

    def execute(self, job):
        self.job = job
        self.broker = job.broker

        switch = {
            Invest.INVEST_DEAL_BUY: self.buy,
            Invest.INVEST_DEAL_SELL: self.sell,
            Invest.INVEST_DEAL_NULL: self.null,
        }

        invest: Invest
        for invest in job.result:
            switch.get(invest.deal, self.null)(invest)

        return True

    def buy(self, invest: Invest):
        if invest.amount == 0:
            return False
        ret = self.broker.buy(invest.code, invest.price, invest.amount)
        information = str(invest) + '\t' + str(ret)
        self.job.notice(information)
        self.job.trade(information)
        return True

    def sell(self, invest: Invest):
        if invest.amount == 0:
            return False
        ret = self.broker.sell(invest.code, invest.price, invest.amount)
        information = str(invest) + '\t' + str(ret)
        self.job.notice(information)
        self.job.trade(information)
        return True

    def null(self, invest):
        return True


def main(argv):
    from .job import Job
    conf = {'name': 'deal', 'switch': 1, 'broker': 'manual', 'portfolio': 'portfolio_template.yaml'}
    job = Job(conf)
    strategy = DealStrategy()
    strategy.execute(job)
    print((job.result.__str__().encode('utf-8')))


if __name__ == "__main__":
    main(sys.argv)
