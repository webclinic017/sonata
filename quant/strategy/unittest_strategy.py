#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: unittest_strategy.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-08 23:38
# @ModifyDate: 2017-04-08 23:38
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
from base_strategy import BaseStrategy
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import unittest
import logging
from unit_test.test_quotation import TestQuotation
from unit_test.HTMLTestRunner import HTMLTestRunner


class UnittestStrategy(BaseStrategy):
    """
    测试sonata依赖的接口
    如果有失败，发送邮件报告
    """

    def __init__(self):
        return

    def execute(self, job):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestQuotation)
        test_result = unittest.TextTestRunner(verbosity=2).run(suite)
        if not test_result.wasSuccessful():
            failure_report = 'FAIL: unittest_strategy failed!\n'
            failure_report += '==================================================\n'
            for failure in test_result.failures:
                for i in range(len(failure)):
                    failure_report += str(failure[i])
                failure_report += '--------------------------------------------------\n'
            #logging.getLogger("smtp").warning(failure_report)
            job.smtp(failure_report)
        return 0

def main(argv):
    job = {}
    job['contex'] = {}
    job['contex']['result'] = ['000401', '600340']
    strategy = UnittestStrategy()
    strategy.execute(job)

if __name__ == "__main__":
    main(sys.argv)
