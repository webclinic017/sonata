#!/usr/bin/python
#-*- coding: utf-8 -*- 

from pyglet.resource import file

import utils.const as CT
import yaml

config_file = CT.CONF_DIR + 'quant.yaml'
with open(config_file, encoding='utf-8') as f:
    config = yaml.safe_load(f)
