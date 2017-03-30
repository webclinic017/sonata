#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: type_converter.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-03-30 23:37
# @ModifyDate: 2017-03-30 23:37
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#
import sys

def to_int(str):
    """
    由字符串转化为int
    """
    value = 0
    try:
        value = int(str)
    except Exception:
        pass

    return value

def to_float(str):
    """
    由字符串转化为float
    """
    value = 0.0
    try:
        value = float(str)
    except Exception:
        pass

    return value


def main(argv):
    print to_int('123')
    print to_int('a23')
    print to_float('1.23')
    print to_float('1.23f')



if __name__ == "__main__":
    main(sys.argv)
