#!/usr/bin/python
#-*- coding: utf-8 -*- 

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
#from trader.trader import Trader

class BaseStrategy:
    """策略基类 """

    def __init__(self):
        return

    def execute(self, job):
        #t = Trader(job.conf['trader'])
        #d = t.balance()
        #for b in d:
        #    for (k,v) in b.items():
        #        print (k + ':' + str(v)).encode('utf-8')

        print((job.result.__str__().encode('utf-8')))
        for p in job.result:
            if p.code == '601288':
                job.result.remove(p)
        print((job.result.__str__().encode('utf-8')))
        return 0


def main(argv):
    strategy = BaseStrategy()
    strategy.execute('')

if __name__ == "__main__":
    main(sys.argv)
