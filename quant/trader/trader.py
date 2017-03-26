#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: trader.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-05-14 15:29
# @ModifyDate: 2016-05-14 15:29
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import easytrader
#from easytrader.helpers import disable_log
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT
#from myhttrader import MyHTTrader
from myxqtrader import MyXueQiuTrader


class Trader:
    """交易类"""

    def __init__(self, broker):
        self.broker = broker
        self.user = self._use(self.broker)

    def balance(self):
        """资金"""
        return self.user.balance()

    def position(self):
        """持仓"""
        return self.user.position()

    def entrust(self):
        """委托单"""
        return self.user.entrust()

    def get_exchangebill(self, start_date, end_date):
        """
        查询指定日期内的交割单
        :param start_date: 20160211
        :param end_date: 20160211
        :return:
        """
        if 'ht' != self.broker:
            return False
        return self.user.get_exchangebill(start_date, end_date)


    def buy(self, stock_code, price=0, amount=0, volume=0, entrust_prop=0):
        """买入卖出股票
        :param stock_code: 股票代码
        :param price: 买入价格
        :param amount: 买入股数
        :param volume: 买入总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop: 雪球直接市价
        """
        return self.user.buy(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def sell(self, stock_code, price, amount=0, volume=0, entrust_prop=0):
        """卖出股票
        :param stock_code: 股票代码
        :param price: 卖出价格
        :param amount: 卖出股数
        :param volume: 卖出总金额 由 volume / price 取整， 若指定 amount 则此参数无效
        :param entrust_prop: 委托类型，暂未实现，默认为限价委托
        """
        return self.user.sell(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def cancel_entrust(self, entrust_no, stock_code=''):
        """撤单
        :param entrust_no: 委托单号
        """
        if 'ht' != self.broker:
            return False
        return self.user.cancel_entrust(entrust_no, stock_code)

    def cancel_all_entrust(self):
        """
        撤单所有委托
        """
        if 'ht' != self.broker:
            return False
        return self.user.cancel_all_entrust()

    def _use(self, broker, debug=True, **kwargs):
        #if not debug:
        #    disable_log()
        if broker.lower() in ['ht', 'HT', '华泰']:
            return MyHTTrader(**kwargs)
        if broker.lower() in ['yjb', 'YJB', '佣金宝']:
            return easytrader.YJBTrader()
        if broker.lower() in ['yh', 'YH', '银河']:
            return easytrader.YHTrader()
        if broker.lower() in ['xq', 'XQ', '雪球']:
            return MyXueQiuTrader()
        if broker.lower() in ['gf', 'GF', '广发']:
            return easytrader.GFTrader()
        return

    #def _prepare(self):
    #    if self.user.valid != True:
    #        #self.user = easytrader.use(self.broker)
    #        self.user = self._use(self.broker)
    #        self.user.prepare(CT.CONF_DIR + 'trader/' + self.broker + '.json')

def main(argv):
    #t = Trader('ht')
    #d = t.balance()
    #d = t.position()
    #d = t.entrust()
    #d = t.get_exchangebill('20160517', '20160520')
    #d = t.buy('601288', price=1.8, volume=1000)
    #d = t.buy('601288', price=2.8, amount=100)
    #d = t.sell('131810', price=1, amount=20)
    #d = t.cancel_entrust('114', '601288')
    #d = t.cancel_all_entrust()

    #####################################################

    t = Trader('xq')
    d = t.balance()
    #d = t.position()
    #d = t.entrust()
    #d = t.buy('601288', price=3.05, amount=100000)
    #d = t.sell('601288', price=3.05, amount=50000)
    #d = t.cancel_entrust('92640488', '601288') #TODO
    #d = t.cancel_all_entrust() #TODO

    print d
    if isinstance(d, list):
        for b in d:
            for (k,v) in b.items():
                print (k + ':' + str(v)).encode('utf-8')
            print '--------------------------------'
    if isinstance(d, dict):
        for (k,v) in d.items():
            print (k + ':' + str(v)).encode('utf-8')

if __name__ == "__main__":
    main(sys.argv)
