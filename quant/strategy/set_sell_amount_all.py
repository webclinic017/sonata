#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: set_sell_amount_all.py
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
from trader.trader import Trader

class SetSellAmountAll(BaseStrategy):
    """
    设置卖出量为所有可卖出股票
    如果已经有委托卖单且价格不一样，则撤销原委托单，重新委托卖出
    """

    def __init__(self):
        return

    def execute(self, job):
        t = Trader.get_instance(job['trader'])

        entrusts = t.check_available_cancels()
        entrust_to_cancle = []
        for invest in job.result[:]:
            for e in entrusts:
                if e.iotype == 'sell' and e.stock_code == invest.code:
                    if e.entrust_price == invest.price:
                        job.result.remove(invest)
                    else:
                        entrust_to_cancle.append(e.entrust_no)

        if len(entrust_to_cancle):
            ret = t.cancel_entrusts(','.join(entrust_to_cancle))
            job.notice(str(ret))
            job.trade(str(ret))
            #不要过于频繁操作
            time.sleep(1)

        position = t.position()
        for i,v in enumerate(job.result):
            #找到该股的持仓数据
            v_position = ''
            for p in position:
                if p.stock_code == v.code:
                    v_position = p
            #没有持仓
            if v_position == '':
                continue

            #设置卖出参数
            job.result[i].amount = v_position.enable_amount

        return 0

def main(argv):
    from job import Job
    conf = {'name':'buy', 'switch':1, 'trader':'yh', 'portfolio': 'portfolio_template.yaml'}
    job = Job(conf)
    strategy = SetSellAmountAll()
    strategy.execute(job)
    print job.result.__str__().encode('utf-8')

if __name__ == "__main__":
    main(sys.argv)
