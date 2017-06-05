#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: const.py 定义常量
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-18 00:11
# @ModifyDate: 2016-04-18 00:14
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#
import os

#目录
HOME = os.path.dirname(os.path.abspath(__file__)) + '/../../'
BASICS_DIR = HOME + 'data/basics/'
HIS_DIR = HOME + 'data/his/'
HFQ_DIR = HOME + 'data/hfq/'
TICK_DIR = HOME + 'data/tick/'
HSGT_DIR = HOME + 'data/hsgt/'
LOG_DIR = HOME + 'log/'
CONF_DIR = HOME + 'conf/'
PORTFOLIO_CONF_DIR = CONF_DIR + 'portfolio/'

#历史数据开始时间
START = '2001-01-01'

#线程数
HIS_THRD_CNT = 10
TICK_THRD_CNT = 10
