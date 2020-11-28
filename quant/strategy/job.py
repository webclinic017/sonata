#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: job.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-09 12:27
# @ModifyDate: 2017-04-09 12:27
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT
import yaml
import logging
import time
from .base_strategy import BaseStrategy
from .unittest_strategy import UnittestStrategy
from .shibor_strategy import ShiborStrategy
from .sell_repos_strategy import SellReposStrategy
from .buy_strategy import BuyStrategy
from .sell_strategy import SellStrategy
from .portfolio import Portfolio
from .buy_nongyeyinhang_strategy import BuyNongyeyinhangStrategy
from .sell_nongyeyinhang_strategy import SellNongyeyinhangStrategy
from .set_sell_amount_all import SetSellAmountAll

class Job():

    def __init__(self, conf):
        self.conf = conf
        self.status = 1
        self.result = Portfolio()
        self.info = []
        self.contex = {}
        self.logid = conf['name'] + '-' + str(int(time.time()))
        if 'portfolio' in list(self.conf.keys()) and self.conf['portfolio'] != None:
            self.result = Portfolio(CT.CONF_DIR + 'portfolio/' + self.conf['portfolio'])
        #if 'portfolio' in self.conf.keys() and self.conf['portfolio'] != None:
        #    portfolio = yaml.load(file(CT.CONF_DIR + 'portfolio/' + self.conf['portfolio']))
        #    self.result = portfolio

    def __getitem__(self, key):
        return self.conf[key]

    def __setitem__(self, key, value):
        self.conf[key] = value

    def __iter__(self):
        return iter(self.conf['strategy'])

    def items(self):
        return list(self.conf['strategy'].items())

    def append(self, strategy):
        self.conf['strategy'].append(strategy)
        return True

    def execute(self):
        #self.notice('JOB[%s][%d:%s]' % (self.logid, self.status, ','.join(self.result)))
        self.notice('JOB[%s][%d:%s]' % (self.logid, self.status, self.result.__str__()))
        for strategy in self.conf['strategies']:
            if strategy['switch'] != 1:
                continue

            self.notice('[%s]' % (strategy['name']))
            self.contex['strategy'] = strategy
            obj = eval(strategy['name'])()
            obj.execute(self)

            #self.notice('[%d:%s]' % (self.status, ','.join(self.result)))
            self.notice('[%d:%s]' % (self.status, self.result.__str__()))
            #job终止
            if self.status == 0:
                break

        logging.getLogger("quant").info(' '.join(self.info))
        return 0

    def notice(self, information):
        """
        打印info信息
        """
        self.info.append(information)
        return 0

    def warn(self, information):
        message = '[%s] %s' % (self.logid, information)
        logging.getLogger("warn").warn(message)
        return 0

    def trade(self, information):
        message = '[%s] %s' % (self.logid, information)
        logging.getLogger("trade").info(message)
        return 0

    def smtp(self, information):
        message = '[%s] %s' % (self.logid, information)
        logging.getLogger("smtp").warning(message)
        return 0

    def format(self, information):
        if isinstance(information, str):
            return information
        info_list = []
        if isinstance(information, list):
            info_list = information
        else:
            info_list.append(information)

        info_str = "["
        for item in info_list:
            info_str += "{"
            for (k,v) in list(item.items()):
                info_str += k + ':' + str(v) + ', '
            info_str += '}, '
        info_str += "]"
        return info_str



def main(argv):
    #conf = {'name':'all repos', 'switch':1, 'trader':'xq', 'portfolio': 'portfolio_template.yaml'}
    #job = Job(conf)
    ##strategy = SellReposStrategy()
    #strategy = BaseStrategy()
    #strategy.execute(job)
    #print job.result.__str__().encode('utf-8')

    conf = {'name':'all repos', 'switch':1, 'trader':'yh', 'portfolio': 'repos.yaml'}
    job = Job(conf)
    strategy = SellReposStrategy()
    strategy.execute(job)
    strategy = SellStrategy()
    strategy.execute(job)
    print((job.result.__str__().encode('utf-8')))


if __name__ == "__main__":
    main(sys.argv)

