#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: symbol.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-27 19:00
# @ModifyDate: 2016-04-27 19:00
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

SH_INDEX_LIST = {'sh':'000001', 'sz50':'000016', 'zh500':'000905'}
SZ_INDEX_LIST = {'sz':'399001', 'hs300':'399300', 'zxb':'399005', 'cyb':'399006', 'zx300':'399008'}

def symbol_of(code):
    """
    生成symbol代码标志
    """
    if code in SH_INDEX_LIST:
        return 'sh' + SH_INDEX_LIST[code]
    elif code in SZ_INDEX_LIST:
        return 'sz' + SZ_INDEX_LIST[code]
    else:
        if exchange_of(code) == 'sh':
            return 'sh' + code
        elif exchange_of(code) == 'sz':
            return 'sz' + code
        return ''

def zs_symbol_of(code):
    """
    生成指数symbol代码标志
    """
    for (k,v) in list(SH_INDEX_LIST.items()):
        return 'sh' + code
    for (k,v) in list(SZ_INDEX_LIST.items()):
        return 'sz' + code

def em_symbol_of(code):
    """
    生成东方财富symbol代码标志
    """
    if code in SH_INDEX_LIST:
        return SH_INDEX_LIST[code] + '1'
    elif code in SZ_INDEX_LIST:
        return SZ_INDEX_LIST[code] + '2'
    else:
        if exchange_of(code) == 'sh':
            return code + '1'
        elif exchange_of(code) == 'sz':
            return code + '2'
        return ''


def ne_symbol_of(code):
    """
    生成网易symbol代码标志
    """
    if code in SH_INDEX_LIST:
        return '0' + SH_INDEX_LIST[code]
    elif code in SZ_INDEX_LIST:
        return '1' + SZ_INDEX_LIST[code]
    else:
        if exchange_of(code) == 'sh':
            return '0' + code
        elif exchange_of(code) == 'sz':
            return '1' + code
        return ''

def exchange_of(code):
    """
    得到证券交易所
    """
    if code in SH_INDEX_LIST:
        return 'sh'
    if code in SZ_INDEX_LIST:
        return 'sz'
    if code[:1] in ['5', '6', '9', '2']:
        return 'sh'
    if len(code) != 6 :
        return ''
    return 'sz'

def code_of(code):
    """
    得到指数的编码，如果不是指数返回原值
    """
    if code in SH_INDEX_LIST:
        return SH_INDEX_LIST[code]
    elif code in SZ_INDEX_LIST:
        return SZ_INDEX_LIST[code]
    return code

def code_from_symbol(symbol):
    """
    从股票symbol得到编码，如是是指数则返回sh
    """
    return _code_index_of(symbol[2:], symbol[:2])

def code_from_em_symbol(em_symbol):
    """
    从东方财富symbol代码标志生成code
    如是是指数则返回sh
    """
    code = em_symbol[:-1]
    if em_symbol[-1:] == "1":
        return _code_index_of(code, 'sh')
    if em_symbol[-1:] == "2":
        return _code_index_of(code, 'sz')

def _code_index_of(code, exchange):
    """
    从指数code得到指数字串sha或股票代码,若非指数则返回""
    """
    code_to_index = {}
    if exchange == 'sh':
        for k, v in list(SH_INDEX_LIST.items()):
            code_to_index[v] = k
    elif exchange == 'sz':
        for k, v in list(SZ_INDEX_LIST.items()):
            code_to_index[v] = k

    if code in code_to_index:
        return code_to_index[code]
    else:
        return code

def is_index(code):
    """
    判断一个代码是否是指数
    """
    if code in SH_INDEX_LIST or code in SZ_INDEX_LIST:
        return True
    else:
        return False

if __name__ == '__main__':
    print((symbol_of('sh')))
    print((symbol_of('000001')))
    print((em_symbol_of('sh')))
    print((em_symbol_of('000001')))
    print((exchange_of('sh')))
    print((exchange_of('cyb')))
    print((exchange_of('000001')))
    print((code_of('sh')))
    print((code_of('000001')))
    print((is_index('000001')))
    print((is_index('sh')))
    print((_code_index_of('000001', 'sh')))
    print((_code_index_of('000001', 'sz')))
    print((code_from_symbol('sh000001')))
    print((code_from_em_symbol('0000011')))
    print((code_from_em_symbol('0000012')))
