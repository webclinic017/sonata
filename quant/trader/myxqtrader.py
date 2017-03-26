#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: myxqtrader.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-19 01:01
# @ModifyDate: 2016-04-19 01:01
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import easytrader
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT

class MyXueQiuTrader(easytrader.XueQiuTrader):
    def __init__(self):
        super(MyXueQiuTrader, self).__init__()
        self.conf = CT.CONF_DIR + 'trader/xq.json'
        self.valid = False

    def balance(self):
        """资金"""
        self.prepare(self.conf)
        return super(MyXueQiuTrader, self).balance
        #return self.balance

    def position(self):
        """持仓"""
        self.prepare(self.conf)
        return super(MyXueQiuTrader, self).position

    def entrust(self):
        """委托单"""
        self.prepare(self.conf)
        return super(MyXueQiuTrader, self).entrust

    def get_exchangebill(self, start_date, end_date):
        """
        查询指定日期内的交割单
        :param start_date: 20160211
        :param end_date: 20160211
        :return:
        """
        self.prepare(self.conf)
        return super(MyXueQiuTrader, self).get_exchangebill(start_date, end_date)

    def buy(self, stock_code, price=0, amount=0, volume=0, entrust_prop=0):
        """买入卖出股票
        :param stock_code: 股票代码
        :param price: 买入价格
        :param amount: 买入股数
        :param volume: 买入总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop: 雪球直接市价
        """
        self.prepare(self.conf)
        return super(MyXueQiuTrader, self).buy(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def sell(self, stock_code, price, amount=0, volume=0, entrust_prop=0):
        """卖出股票
        :param stock_code: 股票代码
        :param price: 卖出价格
        :param amount: 卖出股数
        :param volume: 卖出总金额 由 volume / price 取整， 若指定 amount 则此参数无效
        :param entrust_prop: 委托类型，暂未实现，默认为限价委托
        """
        self.prepare(self.conf)
        return super(MyXueQiuTrader, self).sell(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def cancel_entrust(self, entrust_no, stock_code):
        """撤单
        :param entrust_no: 委托单号
        """
        #TODO
        self.prepare(self.conf)
        return super(MyXueQiuTrader, self).cancel_entrust(long(entrust_no), stock_code)

    def cancel_all_entrust(self):
        """
        撤单所有委托
        """
        #TODO
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
        super(MyXueQiuTrader, self).prepare(need_data)
        self.valid = True
