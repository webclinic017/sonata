#!/usr/bin/python
#-*- coding: utf-8 -*- 

import sys
import os
from pyglet.resource import file
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import yaml
from utils.tool import get_value_by_key
import utils.const as CT

class Invest():
    def __init__(self, conf):
        self.name = get_value_by_key(conf, 'name', '')
        self.code = get_value_by_key(conf, 'code', '')
        self.amount = get_value_by_key(conf, 'amount', 0)
        self.price = get_value_by_key(conf, 'price', 0.0)

    def __str__(self):
        result = '<name: %s, code: %s, amount: %d, price: %f>' % (self.name, self.code, self.amount, self.price)
        return result

class Portfolio():
    def __init__(self, configure = ''):
        self.configure = configure
        self.invest = []
        self.init()

    def __str__(self):
        result = ''
        for item in self.invest:
            result += item.__str__() + ', '
        return result

    def __iter__(self):
        return iter(self.invest)

    def __getitem__(self, key):
        return self.invest[key]

    def __setitem__(self, key, value):
        self.invest[key] = value

    def __len__(self):
        return len(self.invest)

    def items(self):
        return list(self.invest.items())

    def append(self, item):
        if isinstance(item, dict):
            item = Invest(item)
        self.invest.append(item)
        return True

    def remove(self, item):
        self.invest.remove(item)
        return True

    def clear(self):
        self.invest = []
        return True

    def init(self):
        conf = []
        if self.configure != '':
            with open(self.configure, encoding='utf-8') as f:
                conf = yaml.safe_load(f)
            #conf = yaml.load(file(self.configure))
        for c in conf:
            invest = Invest(c)
            self.append(invest)

def main(argv):
    p = Portfolio(CT.CONF_DIR + 'portfolio/' + 'portfolio_template.yaml')

    print((p.__str__().encode('utf-8')))
    p = Portfolio()
    print((p.__str__().encode('utf-8')))
    #print p[0].__str__().encode('utf-8')
    #print (p[0].name + 'aa').encode('utf-8')

    #for port in p:
    #    if port.code == '601288':
    #        p.remove(port)
    #print p.__str__().encode('utf-8')

    return

if __name__ == '__main__':
    main(sys.argv)
