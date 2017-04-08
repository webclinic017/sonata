#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: sell_repos_strategy.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-08 09:53
# @ModifyDate: 2017-04-08 09:53
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
import time
from base_strategy import BaseStrategy
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from quotation.quotation import Quotation

class SellReposStrategy(BaseStrategy):
    """
    逆回购策略
    资金全部购买逆回购
    比较GC001 R-001价格，GC001价格高优先买GC001，不够10W的资金全部买R-001，R-001价格高全部买R-001
    GC003 R-003暂不考虑，周五节价日前价格都比较低，差不多是GC001 R-001的1/3
    """

    def __init__(self):
        return

    def execute(self, job):
        q = Quotation()
        print job

        return 0

def main(argv):
    job = {}
    job['contex'] = {}
    job['contex']['result'] = ['204001', '131810']
    strategy = SellReposStrategy()
    strategy.execute(job)

if __name__ == "__main__":
    main(sys.argv)
