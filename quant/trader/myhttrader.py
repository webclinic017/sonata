#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: myhttrader.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-05-14 15:29
# @ModifyDate: 2016-05-14 15:29
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import easytrader
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT

class MyHTTrader(easytrader.HTTrader):
    def __init__(self, remove_zero=True):
        super(MyHTTrader, self).__init__(remove_zero)
        self.conf = CT.CONF_DIR + 'trader/ht.json'
        self.valid = False

    def balance(self):
        """资金"""
        self.prepare(self.conf)
        return super(MyHTTrader, self).balance
        #return self.balance

    def position(self):
        """持仓"""
        self.prepare(self.conf)
        return super(MyHTTrader, self).position

    def entrust(self):
        """委托单"""
        self.prepare(self.conf)
        return super(MyHTTrader, self).entrust

    def get_exchangebill(self, start_date, end_date):
        """
        查询指定日期内的交割单
        :param start_date: 20160211
        :param end_date: 20160211
        :return:
        """
        self.prepare(self.conf)
        return super(MyHTTrader, self).get_exchangebill(start_date, end_date)

    def buy(self, stock_code, price=0, amount=0, volume=0, entrust_prop=0):
        """买入卖出股票
        :param stock_code: 股票代码
        :param price: 买入价格
        :param amount: 买入股数
        :param volume: 买入总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop: 雪球直接市价
        """
        self.prepare(self.conf)
        return super(MyHTTrader, self).buy(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def sell(self, stock_code, price, amount=0, volume=0, entrust_prop=0):
        """卖出股票
        :param stock_code: 股票代码
        :param price: 卖出价格
        :param amount: 卖出股数
        :param volume: 卖出总金额 由 volume / price 取整， 若指定 amount 则此参数无效
        :param entrust_prop: 委托类型，暂未实现，默认为限价委托
        """
        self.prepare(self.conf)
        return super(MyHTTrader, self).sell(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def cancel_entrust(self, entrust_no, stock_code=''):
        """撤单
        :param entrust_no: 委托单号
        """
        self.prepare(self.conf)
        return super(MyHTTrader, self).cancel_entrust(entrust_no)

    def cancel_all_entrust(self):
        """
        撤单所有委托
        """
        self.prepare(self.conf)
        entrusts = self.entrust()
        if isinstance(entrusts, list):
            for e in entrusts:
                self.cancel_entrust(e['entrust_no'])
        entrusts = self.entrust()
        return entrusts


    def check_account_live(self, response):
        if isinstance(response, list):
            self.valid = True
            return True
        else:
            self.valid = False
            return False

    def prepare(self, need_data):
        if self.valid != True:
            super(MyHTTrader, self).prepare(need_data)
            self.valid = True

def main(argv):
    t = MyHTTrader()
    #d = t.balance()
    #d = t.position()
    d = t.entrust()
    #d = t.get_exchangebill('20160517', '20160520')
    #d = t.buy('601288', price=2.8, volume=1000)
    #d = t.buy('601288', price=2.8, amount=100)
    #d = t.sell('131810', price=2, amount=20)
    #d = t.cancel_entrust('8711')
    #d = t.cancel_all_entrust()


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
