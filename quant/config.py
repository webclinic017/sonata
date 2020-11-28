#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: config.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-10 01:22
# @ModifyDate: 2017-04-10 01:22
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#
from pyglet.resource import file

import utils.const as CT
import yaml

config = yaml.load(file(CT.CONF_DIR + 'quant.yaml'))
