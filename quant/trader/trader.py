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
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT
#from myhttrader import MyHTTrader
from myxqtrader import MyXueQiuTrader
from myyhtrader import MyYHTrader
from config import config
import threading
from info import Info

mutex = threading.Lock()

class Checker():
    def __init__(self):
        """
        检查加锁
        """
        self.status = 0
        mutex.acquire(1)

    def __del__(self):
        """
        解锁
        """
        mutex.release()

class Trader:
    """交易类"""

    __instance = None

    def __init__(self, broker):
        self.broker = broker
        self.user = self._use(self.broker)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                mutex.acquire()
                if not cls.__instance:
                    cls.__instance = super(Trader, cls).__new__(cls, *args, **kwargs)
            finally:
                mutex.release()
        return cls.__instance

    @staticmethod
    def get_instance(broker):
        if Trader.__instance is None:
            Trader.__instance = Trader(broker)
        return Trader.__instance

    def balance(self):
        """资金"""
        info = Info('balance', self.broker)
        information = self.user.balance()
        info.format(information)
        return info

    def position(self):
        """持仓"""
        info = Info('position', self.broker)
        information = self.user.position()
        info.format(information)
        return info

    #def get_exchangebill(self, start_date, end_date):
    #    """
    #    查询指定日期内的交割单
    #    :param start_date: 20160211
    #    :param end_date: 20160211
    #    :return:
    #    目前仅在 华泰子类 中实现, 其余券商需要补充
    #    """
    #    if 'ht' != self.broker:
    #        return False
    #    return self.user.get_exchangebill(start_date, end_date)


    def buy(self, stock_code, price, amount=0, volume=0, entrust_prop='limit'):
        """买入股票
        :param stock_code: 股票代码
        :param price: 买入价格
        :param amount: 买入股数
        :param volume: 买入总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop: 委托类型 'limit' 限价单 , 'market'　市价单, 'market_cancel' 五档即时成交剩余转限制
        市价就是以涨停价申报
        """
        info = Info('buy', self.broker)
        if (config['buy']['switch'] ==1 and (config['buy']['black'] == None or stock_code not in config['buy']['black'])) \
                or (config['buy']['white'] != None and stock_code in config['buy']['white']):
            information = self.user.buy(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)
            info.format(information)
        else:
            info.is_black()
        return info

    def sell(self, stock_code, price, amount=0, volume=0, entrust_prop='limit'):
        """卖出股票
        :param stock_code: 股票代码
        :param price: 卖出价格
        :param amount: 卖出股数
        :param volume: 卖出总金额 由 volume / price 取整， 若指定 amount 则此参数无效
        :param entrust_prop: 委托类型，暂未实现，默认为限价委托
        """
        info = Info('sell', self.broker)
        if (config['sell']['switch'] ==1 and (config['sell']['black'] == None or stock_code not in config['sell']['black'])) \
                or (config['sell']['white'] != None and stock_code in config['sell']['white']):
            information = self.user.sell(stock_code, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)
            info.format(information)
        else:
            info.is_black()
        return info

    def entrust(self):
        """委托单
        委托状态：已报、部成、已报待撤、部成待撤、未报、待报、已成、已撤、部撤、废单
        """
        info = Info('entrust', self.broker)
        information = self.user.entrust()
        info.format(information)
        return info

    def check_available_cancels(self, parsed=True):
        """
        @Contact: Emptyset <21324784@qq.com>
        检查撤单列表
        """
        info = Info('entrust', self.broker)
        information = self.user.check_available_cancels(parsed)
        info.format(information)
        return info


    def cancel_entrust(self, entrust_no, stock_code = ''):
        """撤单
        :param entrust_no: 委托单号
        """
        info = Info('cancel', self.broker)
        if self.broker == 'yh':
            information = self.user.cancel_entrust(entrust_no, stock_code)
        elif self.broker == 'xq':
            #xueqiu cancel 接口不可用
            information = self.user.cancel_entrust(entrust_no, stock_code)
        info.format(information)
        return info

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
        c = Checker()
        info = Info('cancel', self.broker)
        information = self.user.cancel_entrusts(entrust_no)
        info.format(information)
        return info

    def cancel_all_entrust(self):
        """
        撤单所有委托
        """
        #if 'ht' != self.broker:
        #    return False
        info = Info('cancel', self.broker)
        information = self.user.cancel_all_entrust()
        info.format(information)
        return info

    def get_deal(self, date=None):
        """
        @Contact: Emptyset <21324784@qq.com>
        获取历史日成交列表
            e.g.: get_deal( "2016-07-14" )
            如果不传递日期则取的是当天成交列表
            返回值格式与get_current_deal相同
            遇到提示“系统超时请重新登录”或者https返回状态码非200或者其他异常情况会返回False
        """
        c = Checker()
        info = Info('deal', self.broker)
        information = self.user.get_deal(date)
        info.format(information)
        return info


    def _use(self, broker, debug=True, **kwargs):
        #if not self._check():
        #    return None

        #if broker.lower() in ['ht', 'HT', '华泰']:
        #    return MyHTTrader(**kwargs)
        #if broker.lower() in ['yjb', 'YJB', '佣金宝']:
        #    return easytrader.YJBTrader()
        if broker.lower() in ['yh']: #'银河'
            return MyYHTrader(**kwargs)
        if broker.lower() in ['xq']:#'雪球'
            return MyXueQiuTrader()
        if broker.lower() in ['gf']:#'广发'
            return easytrader.GFTrader()
        return None

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

    #t = Trader.get_instance('xq')
    #d = t.balance()
    #d = t.position()
    #d = t.entrust()
    #d = t.buy('601288', price=3.05, amount=50000)
    #d = t.sell('601288', price=3.05, amount=50000)
    #d = t.cancel_entrust('146628492', '601228') #TODO
    #d = t.cancel_all_entrust() #TODO

    ######################################################
    t = Trader.get_instance('yh')
    #d = t.balance()
    #d = t.position()
    #d = t.buy('601288', price=3.1, amount=100)
    #d = t.sell('601288', price=3.5, amount=100)
    #d = t.entrust()
    d = t.check_available_cancels()
    #d = t.cancel_entrust('1090', '601288')
    #d = t.cancel_entrusts('2345,2346')
    #d = t.cancel_all_entrust()
    #d = t.get_deal('2017-04-11')

    print str(d).encode('utf-8')

    #if isinstance(d.raw_data, list):
    #    for b in d.raw_data:
    #        for (k,v) in b.items():
    #            print (k + ':' + str(v)).encode('utf-8')
    #        print '--------------------------------'
    #if isinstance(d.raw_data, dict):
    #    for (k,v) in d.raw_data.items():
    #        print (k + ':' + str(v)).encode('utf-8')



if __name__ == "__main__":
    main(sys.argv)
