#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: date_time.py 定义工具
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-18 00:11
# @ModifyDate: 2016-04-18 00:23
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
import os
import datetime
import time


def get_today_str(format='%Y-%m-%d'):
    """
    取得当天日期的字符串形式 1900-01-01
    """
    return datetime.date.today().strftime(format)

def date_to_str(date, format='%Y-%m-%d'):
    """
    从日期对象得到字符串
    --------
    date: 日期对象
    """
    return date.strftime(format)

def str_to_date(str, format='%Y-%m-%d'):
    """
    从字符串得到日期对象
    --------
    str: 1900-01-01
    """
    return datetime.datetime.strptime(str, format)

def compute_date(date, delta, format='%Y-%m-%d'):
    """
    对日期做加减计算
    --------
    date: string,1900-01-01
    delta: int,-1
    """
    if isinstance(date,str):
        date = str_to_date(date, format)
    return date_to_str(date + datetime.timedelta(days=delta))

def str_to_time(str, format='%Y-%m-%d %H:%M:%S'):
    """
    从字符串得到日期对象
    --------
    str: 1900-01-01 09:30:00
    """
    return datetime.datetime.strptime(str, format)

#def time_to_str_s(time):
#    """
#    从日期对象得到字符串,忽略日期,精确到秒
#    --------
#    date: 日期对象
#    """
#    return time.strftime('%H:%M:%S')

def time_to_str(time, format='%Y-%m-%d %H:%M:%S'):
    """
    从日期对象得到完整日期字符串,精确到秒
    --------
    date: 日期对象
    """
    return time.strftime(format)

#def check_file_expired(file, expire):
#    """
#    检查文档是否过期
#    --------
#    file: 文件路径
#    expire：过期时间(分)
#    """
#    if not os.path.exists(file):
#        return True
#    statinfo = os.stat(file)
#    mtime = statinfo.st_mtime
#    now = time.time()
#    if (now - mtime)/60 > expire:
#        return True
#    else:
#        return False

def get_today_time(hour=0, minute=0, second=0):
    """
    根据小时数,得到当天时间
    """
    now = time.time()
    today_start = now - (now % 86400) + time.timezone
    return today_start + hour * 60 * 60 + minute * 60 + second

def get_exchange_time():
    """
    得到当天已经交易的时间
    """
    exchange_time = 0
    now = time.time()
    if now <= get_today_time(9, 30):
        exchange_time = 0
    elif now <= get_today_time(11, 30):
        exchange_time = now - get_today_time(9, 30)
    elif now <= get_today_time(13):
        exchange_time = 2 * 60 * 60
    elif now <= get_today_time(15):
        exchange_time = 2 * 60 * 60 + now - get_today_time(13)
    elif now > get_today_time(15):
        exchange_time = 4 * 60 * 60

    return exchange_time


def main(argv):
    #d = get_his_data('000001')
    #for date in d.index:
    #    print date

    print((get_today_str()))
    print((date_to_str(datetime.date(2005, 7, 14))))
    print((str_to_date('2016-04-09')))
    print((compute_date('2016-04-09', -3)))
    print((compute_date(datetime.datetime.today(), -3)))
    print((get_today_time(0)))
    print((get_exchange_time()))

if __name__ == "__main__":
    main(sys.argv)
