#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from broker.broker import Broker
import utils.const as CT

class TestBroker(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_balance(self):
        b = Broker(CT.BROKER_NAME_MANUAL)
        d = b.balance()

        self.assertEqual(d[0].status, 'ok')
        #self.assertGreater(d[0].enable_balance, 0)


if __name__ == '__main__':
    #print unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBroker)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    print((test_result.wasSuccessful()))
    #print test_result.failures
    for failure in test_result.failures:
        for i in range(len(failure)):
            print((failure[i]))


    #fp = file('test_report.html','wb')
    #生成报告的Title,描述
    #runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='Python Test Report',description='This  is Python  Report')
    #runner.run(suite)
