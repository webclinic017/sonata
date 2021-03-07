#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import easytrader

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT
from utils.logger import Logger


class XueqiuBroker:
    """雪球交易"""

    def __init__(self):
        self.conf = CT.CONF_DIR + 'broker/xueqiu.json'
        self.valid = False
        self.user = easytrader.use('xq')

    def prepare(self, need_data):
        if not self.valid:
            try:
                self.user.prepare(need_data)
                self.valid = True
            except Exception as e:
                self.valid = False
                Logger.warn('XueqiuBroker.prepare() error, err: ' + str(e))

    def balance(self):
        """资金"""
        self.prepare(self.conf)
        if not self.valid:
            return False
        return self.user.balance

    def position(self):
        """持仓"""
        self.prepare(self.conf)
        if not self.valid:
            return False
        return self.user.position

    def buy(self, stock_code, price, amount=0, volume=0, entrust_prop='limit'):
        """买入股票
        :param stock_code: 股票代码
        :param price: 买入价格
        :param amount: 买入股数
        :param volume: 买入总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop: 委托类型 'limit' 限价单 , 'market'　市价单, 'market_cancel' 五档即时成交剩余转限制
        市价就是以涨停价申报
        """
        self.prepare(self.conf)
        if not self.valid:
            return False

        return self.user.buy(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def sell(self, stock_code, price, amount=0, volume=0, entrust_prop='limit'):
        """卖出股票
        :param stock_code: 股票代码
        :param price: 卖出价格
        :param amount: 卖出股数
        :param volume: 卖出总金额 由 volume / price 取整， 若指定 amount 则此参数无效
        :param entrust_prop: 委托类型，暂未实现，默认为限价委托
        """
        self.prepare(self.conf)
        if not self.valid:
            return False
        return self.user.sell(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def today_entrusts(self):
        """委托单
        委托状态：已报、部成、已报待撤、部成待撤、未报、待报、已成、已撤、部撤、废单
        """
        self.prepare(self.conf)
        if not self.valid:
            return False
        return self.user.get_entrust()

    def cancel_entrust(self, entrust_no):
        """撤单
        :param entrust_no: 委托单号
        """
        self.prepare(self.conf)
        if not self.valid:
            return False
        return self.user.cancel_entrust(entrust_no)


def main(argv):
    Logger.get_instance()
    b = XueqiuBroker()
    #print(b.balance())
    print(b.position())
    #print(b.buy('601288', 3.35, 100))
    #print(b.sell('601288', 3.35, 100))
    #print(b.today_entrusts())
    #print(b.cancel_entrust(234612201))


if __name__ == "__main__":
    main(sys.argv)
