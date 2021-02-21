#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT


class BaseModel:
    """model基类"""
    model_name = 'base'
    model_dir = CT.MODEL_DIR + model_name

    def __init__(self):
        return

    def train(self):
        return

    def load(self):
        return

    def predict(self, code):
        return

