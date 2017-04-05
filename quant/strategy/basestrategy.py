#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: basestrategy.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-05 22:03
# @ModifyDate: 2017-04-05 22:03
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from trader.trader import Trader

class BaseStrategy:
    """策略基类 """

    def __init__(self):
        return

    def execute(self, job):
        t = Trader('xq')
        d = t.balance()
        for b in d:
            for (k,v) in b.items():
                print (k + ':' + str(v)).encode('utf-8')

        return


def main(argv):
    strategy = BaseStrategy()
    strategy.execute('')

if __name__ == "__main__":
    main(sys.argv)
