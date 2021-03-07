#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import threading
import yaml
from .manual_broker import ManualBroker
from .xueqiu_broker import XueqiuBroker
from .info import Info

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT


class Checker():
    def __init__(self):
        """
        检查加锁
        """
        self.__mutex = threading.Lock()
        self.status = 0
        self.__mutex.acquire(1)

    def __del__(self):
        """
        解锁
        """
        self.__mutex.release()


class Broker:
    """交易类"""
    __instance = None

    def __init__(self, broker):
        self.broker = broker
        self.user = self._use(self.broker)
        self.conf = CT.CONF_DIR + 'broker/broker.yaml'
        with open(self.conf, encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            c = Checker()
            if not cls.__instance:
                # cls.__instance = super(Broker, cls).__new__(cls, *args, **kwargs)
                cls.__instance = super(Broker, cls).__new__(cls)
        return cls.__instance

    @staticmethod
    def get_instance(broker):
        if Broker.__instance is None:
            Broker.__instance = Broker(broker)
        return Broker.__instance

    @staticmethod
    def _use(broker, debug=True, **kwargs):
        if broker is None:
            return None
        if broker.lower() in [CT.BROKER_NAME_MANUAL]:  # '手动'
            return ManualBroker(**kwargs)
        if broker.lower() in [CT.BROKER_NAME_XUEQIU]:  # '
            return XueqiuBroker(**kwargs)
        return None

    def balance(self):
        """资金"""
        info = Info(Info.INFO_TYPE_BALANCE, self.broker)
        information = self.user.balance()
        info.format(information)
        return info

    def position(self):
        """持仓"""
        info = Info(Info.INFO_TYPE_POSITION, self.broker)
        information = self.user.position()
        info.format(information)
        return info

    def buy(self, stock_code, price, amount=0, volume=0, entrust_prop='limit'):
        """买入股票
        :param stock_code: 股票代码
        :param price: 买入价格
        :param amount: 买入股数
        :param volume: 买入总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop: 委托类型 'limit' 限价单 , 'market'　市价单, 'market_cancel' 五档即时成交剩余转限制
        市价就是以涨停价申报
        """
        info = Info(Info.INFO_TYPE_STATUS, self.broker)
        buy_conf = self.config['buy']
        # 黑白名单功能大于开关
        if (buy_conf['switch'] == 1 and (buy_conf['black'] is None or stock_code not in buy_conf['black'])) \
                or (buy_conf['white'] is not None and stock_code in buy_conf['white']):
            information = self.user.buy(stock_code, price=price, amount=amount, volume=volume,
                                        entrust_prop=entrust_prop)
            info.format(information)
        else:
            info.set_black()
        return info

    def sell(self, stock_code, price, amount=0, volume=0, entrust_prop='limit'):
        """卖出股票
        :param stock_code: 股票代码
        :param price: 卖出价格
        :param amount: 卖出股数
        :param volume: 卖出总金额 由 volume / price 取整， 若指定 amount 则此参数无效
        :param entrust_prop: 委托类型，暂未实现，默认为限价委托
        """
        info = Info(Info.INFO_TYPE_STATUS, self.broker)
        sell_conf = self.config['sell']
        # 黑白名单功能大于开关
        if (sell_conf['switch'] == 1 and (sell_conf['black'] is None or stock_code not in sell_conf['black'])) \
                or (sell_conf['white'] is not None and stock_code in sell_conf['white']):
            information = self.user.sell(stock_code, price=price, amount=amount, volume=volume,
                                         entrust_prop=entrust_prop)
            info.format(information)
        else:
            info.set_black()
        return info


def main(argv):
    b = Broker(CT.BROKER_NAME_MANUAL)
    d = b.balance()
    #d = b.position()
    #d = b.buy('601288', 3.35, 200)
    #d = b.sell('601288', 3.35, 100)
    print(d)

    #b = Broker(CT.BROKER_NAME_XUEQIU)
    ## d = b.balance()
    #d = b.position()
    ##d = b.buy('601288', 3.35, 200)
    ##d = b.sell('601288', 3.35, 100)
    #print(d)


if __name__ == "__main__":
    main(sys.argv)
