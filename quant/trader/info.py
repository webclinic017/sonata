#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: info.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-15 09:53
# @ModifyDate: 2017-04-15 09:53
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.date_time as date_time
import utils.symbol as symbol

class Status(object):
    def __init__(self, broker):
        self.raw_data = ''
        self.broker = broker
        self.status = 'ok'
        self.msg = ''
        self.entrust_no = ''

    def __str__(self):
        result = '<status:%s, msg:%s, entrust_no:%s>' % (self.status, self.msg, self.entrust_no)
        return result


    def format(self, information):
        if self.broker == 'yh':
            return self.format_yh(information)
        if self.broker == 'xq':
            return self.format_xq(information)

    def format_yh(self, information):
        if information.has_key('result_type') and information['result_type'] == 'error':
            self.status = 'error'
            if information.has_key('result_msg'):
                self.msg = information['result_msg']
        if information.has_key('ordersno'):
            self.entrust_no = information['ordersno']
        if information.has_key('msgok'):
            self.msg = information['msgok']
        if information.has_key('failed') and information['failed'] != '0':
            self.status = 'error'
        return True

    def format_xq(self, information):

        if information.has_key('entrust_no'):
            self.entrust_no = information['entrust_no']
        return True

class Balance(Status):
    def __init__(self, broker):
        super(Balance, self).__init__(broker)
        #balance:可用资金
        self.enable_balance = 0.0

    def __str__(self):
        result = '<Balance enable_balance:%f>' % (self.enable_balance)
        return result


    def format(self, information):
        if self.broker == 'yh':
            return self.format_yh(information)
        if self.broker == 'xq':
            return self.format_xq(information)

    def format_yh(self, information):
        super(Balance, self).format_yh(information)
        if self.status == 'error':
            return 'error'

        if not information.has_key(u'可用资金'):
            return False
        self.enable_balance = information[u'可用资金']
        return True

    def format_xq(self, information):
        super(Balance, self).format_yh(information)
        if self.status == 'error':
            return 'error'

        if not information.has_key(u'current_balance'):
            return False
        self.enable_balance = information[u'current_balance']
        return True


class Position(Status):
    def __init__(self, broker):
        super(Position, self).__init__(broker)
        #position:证券名称
        self.stock_name = ''
        #position:证券代码
        self.stock_code = 0
        #position:当前持仓
        self.current_amount = 0
        #position:股份可用
        self.enable_amount = 0
        #position:参考成本价
        self.keep_cost_price = 0
        #position:参考市价
        self.last_price = 0
        #position:参考盈亏
        self.income_balance = 0
        #position:盈亏比例(%)
        self.income_balance_ratio = 0
        #position:参考市值
        self.market_value = 0

    def __str__(self):
        result = '<Position stock_name:%s, stock_code:%s, current_amount:%d, enable_amount:%d, keep_cost_price:%f, last_price:%f, income_balance:%f, income_balance_ratio:%s, market_value:%f>' \
                % (self.stock_name, self.stock_code, self.current_amount, self.enable_amount, self.keep_cost_price, self.last_price, self.income_balance, self.income_balance_ratio, self.market_value)

        return result


    def format(self, information):
        if self.broker == 'yh':
            return self.format_yh(information)
        if self.broker == 'xq':
            return self.format_xq(information)

    def format_yh(self, information):
        super(Position, self).format_yh(information)
        if self.status == 'error':
            return 'error'

        self.stock_name = information[u'证券名称']
        self.stock_code = information[u'证券代码']
        self.current_amount = information[u'当前持仓']
        self.enable_amount = information[u'股份可用']
        self.keep_cost_price = information[u'参考成本价']
        self.last_price = information[u'参考市价']
        self.income_balance = information[u'参考盈亏']
        self.income_balance_ratio = information[u'盈亏比例(%)']
        self.market_value = information[u'参考市值']

        return True

    def format_xq(self, information):
        super(Position, self).format_yh(information)
        if self.status == 'error':
            return 'error'

        self.stock_name = information[u'stock_name']
        self.stock_code = symbol.code_from_symbol(information[u'stock_code'])
        self.current_amount = information[u'current_amount']
        self.enable_amount = information[u'enable_amount']
        self.keep_cost_price = information[u'keep_cost_price']
        self.last_price = information[u'last_price']
        self.income_balance = information[u'income_balance']
        self.income_balance_ratio = information[u'income_balance'] #TODO
        self.market_value = information[u'market_value']

        return True


class Entrust(Status):
    def __init__(self, broker):
        super(Entrust, self).__init__(broker)
        #委托序号
        self.entrust_no = ''
        #状态说明
        #委托状态：已报、部成、已报待撤、部成待撤、未报、待报、已成、已撤、部撤、废单
        self.entrust_status = ''
        #证券名称
        self.stock_name = ''
        #证券代码
        self.stock_code = ''
        #委托价格
        self.entrust_price = 0.0
        #委托数量
        self.entrust_amount = 0
        #成交数量
        self.business_amount = 0
        #委托时间
        self.time = 0

    def __str__(self):
        result = '<Entrust entrust_no:%s, entrust_status:%s, stock_name:%s, stock_code:%s, entrust_price:%f, entrust_amount:%d, business_amount:%d, time:%s>' \
                % (self.entrust_no, self.entrust_status, self.stock_name, self.stock_code, self.entrust_price, self.entrust_amount, self.business_amount, date_time.time_to_str(self.time, '%H:%M:%S'))

        return result


    def format(self, information):
        if self.broker == 'yh':
            return self.format_yh(information)
        if self.broker == 'xq':
            return self.format_xq(information)

    def format_yh(self, information):
        super(Entrust, self).format_yh(information)
        if self.status == 'error':
            return 'error'

        if information.has_key(u'委托序号'):
            self.entrust_no = information[u'委托序号']
            self.entrust_status = information[u'状态说明']
            self.stock_name = information[u'证券名称']
            self.stock_code = information[u'证券代码']
            self.entrust_price = information[u'委托价格']
            self.entrust_amount = information[u'委托数量']
            self.business_amount = information[u'成交数量']
            self.time = date_time.str_to_date(information[u'委托时间'], '%H:%M:%S')
        else:
            self.entrust_no = information[u'entrust_num']
            self.entrust_status = information[u'status']
            self.stock_name = information[u'name']
            self.stock_code = information[u'code']
            self.entrust_price = information[u'price']
            self.entrust_amount = information[u'volume']
            self.business_amount = information[u'trans_vol']
            self.time = date_time.str_to_date(information[u'time'], '%H:%M:%S')

        return True

    def format_xq(self, information):
        super(Entrust, self).format_yh(information)
        if self.status == 'error':
            return 'error'

        self.entrust_no = information[u'entrust_no']
        self.entrust_status = information[u'entrust_status']
        self.stock_name = information[u'stock_name']
        self.stock_code = symbol.code_from_symbol(information[u'stock_code'])
        self.entrust_price = information[u'entrust_price']
        self.entrust_amount = information[u'entrust_amount']
        self.business_amount = information[u'business_amount']
        self.time = date_time.str_to_date(information[u'report_time'], '%Y-%m-%d %H:%M:%S')

        return True


class Deal(Status):
    def __init__(self, broker):
        super(Deal, self).__init__(broker)
        #委托序号
        #当天的成交有 委托序号
        self.entrust_no = ''
        #证券名称
        self.stock_name = ''
        #证券代码
        self.stock_code = ''
        #成交价格
        self.business_price = 0.0
        #成交数量
        self.business_amount = 0
        #成交日期 成交时间
        self.time = 0

    def __str__(self):
        result = '<Deal entrust_no:%s, stock_name:%s, stock_code:%s, business_price:%f, business_amount:%d, time:%s>' \
                % (self.entrust_no, self.stock_name, self.stock_code, self.business_price,self.business_amount, date_time.time_to_str(self.time))

        return result


    def format(self, information):
        if self.broker == 'yh':
            return self.format_yh(information)

    def format_yh(self, information):
        super(Deal, self).format_yh(information)
        if self.status == 'error':
            return 'error'

        #当天的成交有 委托序号
        if information.has_key(u'委托序号'):
            self.entrust_no = information[u'委托序号']
        self.stock_name = information[u'证券名称']
        self.stock_code = information[u'证券代码']
        self.business_price= information[u'成交价格']
        self.business_amount = information[u'成交数量']
        self.time = date_time.str_to_date(information[u'成交日期']+information[u'成交时间'], '%Y%m%d%H:%M:%S')

        return True



class Info():
    def __init__(self, type, broker = 'yh'):
        self.raw_data = ''
        self.type = type
        self.broker = broker
        self.items = []

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, value):
        self.items[key] = value

    def __len__(self):
        return len(self.items)

    def items(self):
        return self.items.items()

    def append(self, item):
        self.items.append(item)
        return True

    def __str__(self):
        result = ''
        for item in self.items:
            result += item.__str__() + '\n'
        return result

    def format(self, raw_data):
        self.raw_data = raw_data
        info_list = []
        if isinstance(raw_data, list):
            info_list = raw_data
        else:
            info_list.append(raw_data)

        for information in info_list:
            if self.type == 'balance':
                item = Balance(self.broker)
            elif self.type == 'position':
                item = Position(self.broker)
            elif self.type == 'entrust':
                item = Entrust(self.broker)
            elif self.type == 'deal':
                item = Deal(self.broker)
            else:
                item = Status(self.broker)
            item.format(information)
            self.append(item)

        return True

    def is_black(self):
        item = Status(self.broker)
        item.status = 'black'
        self.items.append(item)
        return True
