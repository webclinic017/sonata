#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: myyhtrader.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-10 15:29
# @ModifyDate: 2017-04-10 15:29
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import easytrader
import sys
import os
import time
import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT

class MyYHTrader(easytrader.YHTrader):
    def __init__(self, remove_zero=True):
        super(MyYHTrader, self).__init__(remove_zero)
        self.conf = CT.CONF_DIR + 'trader/yh.json'
        self.prepare(self.conf)

    def balance(self):
        """资金"""
        result = False
        exception = False

        if self.s == None:
            self.prepare(self.conf)
        try:
            retry = 0
            while(result == False and retry < 3):
                result = super(MyYHTrader, self).balance
                retry += 1
                time.sleep(1)
        except Exception, e:
            exception = e

        if result == False or exception != False:
            logging.warning('trader error, relogin and retry, err: ' + str(exception))
            self.prepare(self.conf)
            result = super(MyYHTrader, self).balance
        return result

        #if self.s == None:
        #    self.prepare(self.conf)
        #try:
        #    return super(MyYHTrader, self).balance
        #except Exception, e:
        #    logging.warning(e)
        #    self.prepare(self.conf)
        #    return super(MyYHTrader, self).balance

    def position(self):
        """持仓"""
        if self.s == None:
            self.prepare(self.conf)
        try:
            return super(MyYHTrader, self).position
        except Exception, e:
            logging.warning(e)
            self.prepare(self.conf)
            return super(MyYHTrader, self).position

    def entrust(self):
        """委托单"""
        if self.s == None:
            self.prepare(self.conf)
        try:
            return super(MyYHTrader, self).entrust
        except Exception, e:
            logging.warning(e)
            self.prepare(self.conf)
            return super(MyYHTrader, self).entrust

    def buy(self, stock_code, price, amount=0, volume=0, entrust_prop='limit'):
        """买入股票
        :param stock_code: 股票代码
        :param price: 买入价格
        :param amount: 买入股数
        :param volume: 买入总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop: 委托类型 'limit' 限价单 , 'market'　市价单, 'market_cancel' 五档即时成交剩余转限制
        市价就是以涨停价申报
        """
        if self.s == None:
            self.prepare(self.conf)
        try:
            return super(MyYHTrader, self).buy(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)
        except Exception, e:
            logging.warning(e)
            self.prepare(self.conf)
            return super(MyYHTrader, self).buy(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def sell(self, stock_code, price, amount=0, volume=0, entrust_prop='limit'):
        """卖出股票
        :param stock_code: 股票代码
        :param price: 卖出价格
        :param amount: 卖出股数
        :param volume: 卖出总金额 由 volume / price 取整， 若指定 amount 则此参数无效
        :param entrust_prop: str 委托类型 'limit' 限价单 , 'market'　市价单, 'market_cancel' 五档即时成交剩余转限制
        """
        if self.s == None:
            self.prepare(self.conf)
        try:
            return super(MyYHTrader, self).sell(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)
        except Exception, e:
            logging.warning(e)
            self.prepare(self.conf)
            return super(MyYHTrader, self).sell(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def check_available_cancels(self, parsed=True):
        """
        @Contact: Emptyset <21324784@qq.com>
        检查撤单列表
        """
        try:
            return super(MyYHTrader, self).check_available_cancels(parsed)
        except Exception, e:
            logging.warning(e)
            self.prepare(self.conf)
            return super(MyYHTrader, self).check_available_cancels(parsed)

    def cancel_entrust(self, entrust_no, stock_code):
        """撤单
        :param entrust_no: 委托单号
        """
        if self.s == None:
            self.prepare(self.conf)
        try:
            return super(MyYHTrader, self).cancel_entrust(entrust_no, stock_code)
        except Exception, e:
            logging.warning(e)
            self.prepare(self.conf)
            return super(MyYHTrader, self).cancel_entrust(entrust_no, stock_code)

    def cancel_entrusts(self, entrust_no):
        """
        @Contact: Emptyset <21324784@qq.com>
        批量撤单
        @param
            entrust_no: string类型
                        委托单号，用逗号隔开
                        e.g:"8000,8001,8002"
        @return
            返回格式是list，比如一个22个单子的批量撤单
            e.g.:
            [{"success":15, "failed":0},{"success":7, "failed":0}]
        """
        if self.s == None:
            self.prepare(self.conf)
        return super(MyYHTrader, self).cancel_entrusts(entrust_no)


    def cancel_all_entrust(self):
        """
        撤单所有委托
        """
        if self.s == None:
            self.prepare(self.conf)
        entrusts= self.check_available_cancels()
        entrust_list = []
        if isinstance(entrusts, list):
            for e in entrusts:
                entrust_list.append(e['entrust_num'])

        entrusts = self.cancel_entrusts(','.join(entrust_list))
        return entrusts

    def get_current_deal(self, date=None):
        """
        获取当日成交列表.
        """
        if self.s == None:
            self.prepare(self.conf)
        try:
            return super(MyYHTrader, self).get_current_deal(date)
        except Exception, e:
            logging.warning(e)
            self.prepare(self.conf)
            return super(MyYHTrader, self).get_current_deal(date)

    def get_deal(self, date=None):
        """
        @Contact: Emptyset <21324784@qq.com>
        获取历史日成交列表
            e.g.: get_deal( "2016-07-14" )
            如果不传递日期则取的是当天成交列表
            返回值格式与get_current_deal相同
            遇到提示“系统超时请重新登录”或者https返回状态码非200或者其他异常情况会返回False
        """
        if self.s == None:
            self.prepare(self.conf)
        ret =  super(MyYHTrader, self).get_deal(date)
        if ret != False:
            return ret
        logging.warning('get_deal error')
        self.prepare(self.conf)
        return super(MyYHTrader, self).get_deal(date)

    def prepare(self, need_data):
        super(MyYHTrader, self).prepare(need_data)

def main(argv):
    t = MyYHTrader()
    d = t.balance()
    #d = t.position()
    #d = t.buy('601288', price=3.1, amount=100)
    #d = t.sell('131810', price=2, amount=10)
    #d = t.sell('601288', price=3.3, amount=100)
    #d = t.entrust()
    #d = t.check_available_cancels()
    #d = t.cancel_entrust('505819', '601288')
    #d = t.cancel_entrusts('508370,508995')
    #d = t.cancel_all_entrust()
    #d = t.get_current_deal()
    #d = t.get_deal()


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
