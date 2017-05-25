#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: test_quotation.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-08 22:52
# @ModifyDate: 2017-04-08 22:52
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from quotation.quotation import Quotation
import HTMLTestRunner,StringIO

class TestQuotation(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_realtime_quotes(self):
        q = Quotation()
        d = q.get_realtime_quotes('sh')
        self.assertIn('sh', d)
        self.assertEqual(d['sh'].symbol, 'sh000001')
        self.assertEqual(d['sh'].code, 'sh')
        self.assertEqual(d['sh'].name, u'上证指数')

        d = q.get_realtime_quotes(['000002', '601992'])
        self.assertIn('000002', d)
        self.assertIn('601992', d)

    def test_get_one_realtime_quotes(self):
        q = Quotation()
        d = q.get_one_realtime_quotes('131800')
        self.assertIn('131800', d)
        self.assertEqual(d['131800'].symbol, 'sz131800')
        self.assertEqual(d['131800'].code, '131800')

    def test_get_today_ticks(self):
        q = Quotation()
        d = q.get_today_ticks('sh')
        self.assertEqual(d.symbol, 'sh000001')

    def test_get_stock_basics(self):
        q = Quotation()
        d = q.get_stock_basics()
        self.assertIn('name', d)
        self.assertGreater(len(d), 1000)

    def test_get_tick_data(self):
        q = Quotation()
        d = q.get_tick_data('000001', '2016-05-20')
        self.assertTrue(len(d) > 100)

    def test_get_today_shibor_ON(self):
        q = Quotation()
        d = q.get_today_shibor_ON
        self.assertTrue(d > 0)

    def test_get_hgt_capital(self):
        q = Quotation()
        d = q.get_hgt_capital()
        self.assertTrue(isinstance(d, float))

if __name__ == '__main__':
    #print unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQuotation)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    print test_result.wasSuccessful()
    #print test_result.failures
    for failure in test_result.failures:
        for i in range(len(failure)):
            print failure[i]


    #fp = file('test_report.html','wb')
    #生成报告的Title,描述
    #runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='Python Test Report',description='This  is Python  Report')
    #runner.run(suite)
