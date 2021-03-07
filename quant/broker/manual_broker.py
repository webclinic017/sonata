#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import yaml

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT
from utils.logger import Logger


class ManualBroker:
    BALANCE = 'balance'
    POSITION = 'position'

    """手动交易"""

    def __init__(self):
        self.conf = CT.CONF_DIR + 'broker/manual.yaml'
        self.valid = False
        self.data = None

    def prepare(self, need_data):
        if not self.valid:
            try:
                with open(need_data, encoding='utf-8') as f:
                    self.data = yaml.safe_load(f)
                self.valid = True
            except Exception as e:
                Logger.warn('ManualBroker.prepare() parse manual.yaml error, err: ' + str(e))

    def balance(self):
        """资金"""
        self.prepare(self.conf)
        if self.data is None:
            return False
        return self.data[ManualBroker.BALANCE]

    def position(self):
        """持仓"""
        self.prepare(self.conf)
        if self.data is None:
            return False
        return self.data[ManualBroker.POSITION]

    def buy(self, stock_code, price, amount=0, volume=0, entrust_prop='limit'):
        """买入股票
        :param stock_code: 股票代码
        :param price: 买入价格
        :param amount: 买入股数
        :param volume: 买入总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop: 委托类型 'limit' 限价单 , 'market'　市价单, 'market_cancel' 五档即时成交剩余转限制
        市价就是以涨停价申报
        """
        message = 'MANUAL_BROKER BUY <code: %s, price: %f, amount: %d, volume: %f>' % (stock_code, price, amount, volume)
        Logger.smtp(message)
        return True

    def sell(self, stock_code, price, amount=0, volume=0, entrust_prop='limit'):
        """卖出股票
        :param stock_code: 股票代码
        :param price: 卖出价格
        :param amount: 卖出股数
        :param volume: 卖出总金额 由 volume / price 取整， 若指定 amount 则此参数无效
        :param entrust_prop: 委托类型，暂未实现，默认为限价委托
        """
        message = 'MANUAL_BROKER SELL <code: %s, price: %f, amount: %d, volume: %f>' % (stock_code, price, amount, volume)
        Logger.smtp(message)
        return True


def main(argv):
    b = ManualBroker()
    #print(b.balance())
    #print(b.position())

    #b.buy('601288', 3.5, 100)
    b.sell('601288', 3.5, 100)


if __name__ == "__main__":
    main(sys.argv)
