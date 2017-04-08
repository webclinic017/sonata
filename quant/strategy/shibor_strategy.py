#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: shiborstrategy.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-06 23:54
# @ModifyDate: 2017-04-06 23:54
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
from base_strategy import BaseStrategy
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from quotation.quotation import Quotation

class ShiborStrategy(BaseStrategy):
    """
    shibor 行情策略
    当天隔夜利率过高不买进
    例外：季末例行缺钱
    """

    def __init__(self):
        return

    def execute(self, job):
        print job
        q = Quotation()
        shibor_ON = q.get_today_shibor_ON()
        job['contex']['status'] = 0

        return 0

def main(argv):
    job = {}
    job['contex'] = {}
    job['contex']['result'] = ['000401', '600340']
    strategy = ShiborStrategy()
    strategy.execute(job)

if __name__ == "__main__":
    main(sys.argv)
