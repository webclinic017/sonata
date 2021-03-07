#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.date_time as date_time
import utils.symbol as symbol
import utils.const as CT
from utils.logger import Logger


class Status(object):
    STATUS_OK = 'ok'
    STATUS_ERR = 'error'
    STATUS_BLACK = 'black'

    def __init__(self, broker):
        self.raw_data = ''
        self.broker = broker
        self.status = Status.STATUS_OK
        self.msg = ''
        self.entrust_no = ''

    def __str__(self):
        result = '<status:%s, msg:%s, entrust_no:%s>' % (self.status, self.msg, self.entrust_no)
        return result

    def format(self, information):
        if self.broker == CT.BROKER_NAME_MANUAL:
            return self.format_manual(information)
        if self.broker == CT.BROKER_NAME_YINHE:
            return self.format_yh(information)
        if self.broker == CT.BROKER_NAME_XUEQIU:
            return self.format_xq(information)

    def format_manual(self, information):
        return True

    def format_yh(self, information):
        if 'result_type' in information and information['result_type'] == 'error':
            self.status = Status.STATUS_ERR
            if 'result_msg' in information:
                self.msg = information['result_msg']
        if 'ordersno' in information:
            self.entrust_no = information['ordersno']
        if 'msgok' in information:
            self.msg = information['msgok']
        if 'failed' in information and information['failed'] != '0':
            self.status = Status.STATUS_ERR
        return True

    def format_xq(self, information):

        if 'entrust_no' in information:
            self.entrust_no = information['entrust_no']
        return True


class Balance(Status):
    def __init__(self, broker):
        super(Balance, self).__init__(broker)
        # current_balance:现金总额
        self.current_balance = 0.0
        # enable_balance:可用资金
        self.enable_balance = 0.0
        # market_value:参考市值
        self.market_value = 0

    def __str__(self):
        result = '<Balance current_balance:%f, enable_balance:%f, market_val:%f>'\
                 % (self.current_balance, self.enable_balance, self.market_value)
        return result

    def format(self, information):
        if self.broker == CT.BROKER_NAME_MANUAL:
            return self.format_manual(information)
        if self.broker == CT.BROKER_NAME_YINHE:
            return self.format_yh(information)
        if self.broker == CT.BROKER_NAME_XUEQIU:
            return self.format_xq(information)

    def format_manual(self, information):
        try:
            self.current_balance = information['enable_balance']
            self.enable_balance = information['enable_balance']
            self.market_value = information['market_value']
        except Exception as e:
            Logger.warn('Balance.format_manual()  error, err: ' + str(e))

        return True

    def format_yh(self, information):
        super(Balance, self).format_yh(information)
        if self.status == Status.STATUS_ERR:
            return False

        if '可用资金' not in information:
            return False
        self.enable_balance = information['可用资金']
        return True

    def format_xq(self, information):
        super(Balance, self).format_yh(information)
        if self.status == Status.STATUS_ERR:
            return False

        if 'current_balance' not in information:
            return False
        self.current_balance = information['current_balance']
        self.enable_balance = information['current_balance']
        self.market_value = information['market_value']
        return True


class Position(Status):
    def __init__(self, broker):
        super(Position, self).__init__(broker)
        # position:证券名称
        self.stock_name = ''
        # position:证券代码
        self.stock_code = 0
        # position:当前持仓
        self.current_amount = 0
        # position:股份可用
        self.enable_amount = 0
        # position:参考成本价
        self.keep_cost_price = 0
        # position:参考市价
        self.last_price = 0
        # position:参考盈亏
        self.income_balance = 0
        # position:盈亏比例(%)
        self.income_balance_ratio = 0
        # position:参考市值
        self.market_value = 0

    def __str__(self):
        result = '<Position stock_name:%s, stock_code:%s, current_amount:%d, enable_amount:%d, keep_cost_price:%f, ' \
                 'last_price:%f, income_balance:%f, income_balance_ratio:%s, market_value:%f>' \
                 % (self.stock_name, self.stock_code, self.current_amount, self.enable_amount, self.keep_cost_price,
                    self.last_price, self.income_balance, self.income_balance_ratio, self.market_value)

        return result

    def format(self, information):
        if self.broker == CT.BROKER_NAME_MANUAL:
            return self.format_manual(information)
        if self.broker == CT.BROKER_NAME_YINHE:
            return self.format_yh(information)
        if self.broker == CT.BROKER_NAME_XUEQIU:
            return self.format_xq(information)

    def format_manual(self, information):
        try:
            self.stock_name = information['stock_name']
            self.stock_code = information['stock_code']
            self.current_amount = information['current_amount']
            self.enable_amount = information['enable_amount']
        except Exception as e:
            Logger.warn('Position.format_manual()  error, err: ' + str(e))

        return True

    def format_yh(self, information):
        super(Position, self).format_yh(information)
        if self.status == Status.STATUS_ERR:
            return False

        self.stock_name = information['证券名称']
        self.stock_code = information['证券代码']
        self.current_amount = information['当前持仓']
        self.enable_amount = information['股份可用']
        self.keep_cost_price = information['参考成本价']
        self.last_price = information['参考市价']
        self.income_balance = information['参考盈亏']
        self.income_balance_ratio = information['盈亏比例(%)']
        self.market_value = information['参考市值']

        return True

    def format_xq(self, information):
        super(Position, self).format_yh(information)
        if self.status == Status.STATUS_ERR:
            return False

        self.stock_name = information['stock_name']
        self.stock_code = symbol.code_from_symbol(information['stock_code'])
        self.current_amount = information['current_amount']
        self.enable_amount = information['enable_amount']
        self.keep_cost_price = information['keep_cost_price']
        self.last_price = information['last_price']
        self.income_balance = information['income_balance']
        self.income_balance_ratio = information['income_balance']  # TODO
        self.market_value = information['market_value']

        return True


class Entrust(Status):
    def __init__(self, broker):
        super(Entrust, self).__init__(broker)
        # 委托序号
        self.entrust_no = ''
        # 状态说明
        # 委托状态：已报、部成、已报待撤、部成待撤、未报、待报、已成、已撤、部撤、废单
        self.entrust_status = ''
        # 证券名称
        self.stock_name = ''
        # 证券代码
        self.stock_code = ''
        # 委托价格
        self.entrust_price = 0.0
        # 委托数量
        self.entrust_amount = 0
        # 成交数量
        self.business_amount = 0
        # 委托类型
        self.iotype = ''
        # 委托时间, 买入、卖出  buy、sell
        self.time = 0

    def __str__(self):
        result = '<Entrust entrust_no:%s, entrust_status:%s, stock_name:%s, stock_code:%s, entrust_price:%f, ' \
                 'entrust_amount:%d, business_amount:%d, iotype:%s, time:%s>' \
                 % (self.entrust_no, self.entrust_status, self.stock_name, self.stock_code, self.entrust_price,
                    self.entrust_amount, self.business_amount, self.iotype,
                    date_time.time_to_str(self.time, '%H:%M:%S'))

        return result

    def format(self, information):
        if self.broker == CT.BROKER_NAME_YINHE:
            return self.format_yh(information)
        if self.broker == CT.BROKER_NAME_XUEQIU:
            return self.format_xq(information)

    def format_yh(self, information):
        super(Entrust, self).format_yh(information)
        if self.status == Status.STATUS_ERR:
            return False

        if '委托序号' in information:
            self.entrust_no = information['委托序号']
            self.entrust_status = information['状态说明']
            self.stock_name = information['证券名称']
            self.stock_code = information['证券代码']
            self.entrust_price = information['委托价格']
            self.entrust_amount = information['委托数量']
            self.business_amount = information['成交数量']
            if information['买卖标志'] == '买入':
                self.iotype = 'buy'
            elif information['买卖标志'] == '卖出':
                self.iotype = 'sell'
            self.time = date_time.str_to_date(information['委托时间'], '%H:%M:%S')
        else:
            self.entrust_no = information['entrust_num']
            self.entrust_status = information['status']
            self.stock_name = information['name']
            self.stock_code = information['code']
            self.entrust_price = information['price']
            self.entrust_amount = information['volume']
            self.business_amount = information['trans_vol']
            if information['iotype'] == '买入':
                self.iotype = 'buy'
            elif information['iotype'] == '卖出':
                self.iotype = 'sell'
            self.time = date_time.str_to_date(information['time'], '%H:%M:%S')

        return True

    def format_xq(self, information):
        super(Entrust, self).format_yh(information)
        if self.status == Status.STATUS_ERR:
            return False

        self.entrust_no = information['entrust_no']
        self.entrust_status = information['entrust_status']
        self.stock_name = information['stock_name']
        self.stock_code = symbol.code_from_symbol(information['stock_code'])
        self.entrust_price = information['entrust_price']
        self.entrust_amount = information['entrust_amount']
        self.business_amount = information['business_amount']
        self.time = date_time.str_to_date(information['report_time'], '%Y-%m-%d %H:%M:%S')

        return True


class Deal(Status):
    def __init__(self, broker):
        super(Deal, self).__init__(broker)
        # 委托序号
        # 当天的成交有 委托序号
        self.entrust_no = ''
        # 证券名称
        self.stock_name = ''
        # 证券代码
        self.stock_code = ''
        # 成交价格
        self.business_price = 0.0
        # 成交数量
        self.business_amount = 0
        # 成交日期 成交时间
        self.time = 0

    def __str__(self):
        result = '<Deal entrust_no:%s, stock_name:%s, stock_code:%s, business_price:%f, business_amount:%d, time:%s>' \
                 % (self.entrust_no, self.stock_name, self.stock_code, self.business_price, self.business_amount,
                    date_time.time_to_str(self.time))

        return result

    def format(self, information):
        if self.broker == CT.BROKER_NAME_YINHE:
            return self.format_yh(information)

    def format_yh(self, information):
        super(Deal, self).format_yh(information)
        if self.status == CT.BROKER_NAME_YINHE:
            return False

        # 当天的成交有 委托序号
        if '委托序号' in information:
            self.entrust_no = information['委托序号']
        self.stock_name = information['证券名称']
        self.stock_code = information['证券代码']
        self.business_price = information['成交价格']
        self.business_amount = information['成交数量']
        self.time = date_time.str_to_date(information['成交日期'] + information['成交时间'], '%Y%m%d%H:%M:%S')

        return True


class Info:
    INFO_TYPE_BALANCE = 'balance'
    INFO_TYPE_POSITION = 'position'
    INFO_TYPE_ENTRUST = 'entrust'
    INFO_TYPE_DEAL = 'deal'
    INFO_TYPE_STATUS = 'status'

    def __init__(self, type, broker):
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
        return list(self.items.items())

    def append(self, item):
        self.items.append(item)
        return True

    def __str__(self):
        result = ''
        for item in self.items:
            result += item.__str__() + '\n'
        return result

    def format(self, raw_data):
        print('format raw_data:\n' + str(raw_data) + '\n', file=sys.stderr)

        self.raw_data = raw_data
        info_list = []
        if isinstance(raw_data, list):
            info_list = raw_data
        else:
            info_list.append(raw_data)

        for information in info_list:
            if self.type == Info.INFO_TYPE_BALANCE:
                item = Balance(self.broker)
            elif self.type == Info.INFO_TYPE_POSITION:
                item = Position(self.broker)
            elif self.type == Info.INFO_TYPE_ENTRUST:
                item = Entrust(self.broker)
            elif self.type == Info.INFO_TYPE_DEAL:
                item = Deal(self.broker)
            else:
                item = Status(self.broker)
            item.format(information)
            self.append(item)

        return True

    def set_black(self):
        item = Status(self.broker)
        item.status = Status.STATUS_BLACK
        self.items.append(item)
        return True
