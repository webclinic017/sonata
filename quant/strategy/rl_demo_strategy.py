#!/usr/bin/python
#-*- coding: utf-8 -*- 

import sys
import os
import time
from .base_strategy import BaseStrategy
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
#from trader.trader import Trader
import copy
from model.demo_model import DemoModel


class RlDemoStrategy(BaseStrategy):
    """
    """

    def __init__(self):
        return

    def execute(self, job):
        m = DemoModel()
        temp_result = copy.copy(job.result)
        job.result.clear()
        for i, v in enumerate(temp_result):
            code = v.code
            m.predict(code)
        return 0

def main(argv):
    from .job import Job
    conf = {'name': 'rl_demo', 'switch': 1, 'broker': 'yh', 'portfolio': 'nongyeyinhang.yaml'}
    job = Job(conf)
    strategy = RlDemoStrategy()
    strategy.execute(job)
    print((job.status))
    print((job.result.__str__().encode('utf-8')))

if __name__ == "__main__":
    main(sys.argv)
