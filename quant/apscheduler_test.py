#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: quant.py
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-05-19 00:46
# @ModifyDate: 2016-05-19 00:46
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from trader.trader import Trader
import utils.const as CT
import yaml

t = Trader('xq')

def my_job(conf):
    print conf
    global t
    #d = t.sell('131810', price=1, amount=20)
    d = t.balance()
    print d
    for b in d:
        for (k,v) in b.items():
            print (k + ':' + str(v)).encode('utf-8')

def add_job(sched):
    #sched.add_job(my_job, 'interval', seconds=5)
    #sched.add_job(my_job, 'cron', second='*/30', args = [CT.CONF_DIR + 'trader/ht.json'])
    #sched.add_job(my_job, 'cron', minute = 10, hour = 13, args = [CT.CONF_DIR + 'trader/ht.json'])
    #sched.add_job(my_job, 'cron', second='*/30', minute='*', hour='*', day='*', month='*', year='*', day_of_week='*', args = [CT.CONF_DIR + 'trader/xq.json'])
    conf = yaml.load(file(CT.CONF_DIR + 'quant.yaml'))
    sched.add_job(eval(conf['input']), 'cron', second='*/10', minute='*', hour='*', day='*', month='*', year='*', day_of_week='*', args = [CT.CONF_DIR + 'trader/xq.json'])
    return


def main(argv):
    jobstores = {'default':MemoryJobStore()}
    executors = {
        'default': ThreadPoolExecutor(10),
        #'processpool': ProcessPoolExecutor(3)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }

    sched = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
#    #sched = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
#    #sched = BlockingScheduler()
#
#    #sched.add_job(my_job, 'interval', seconds=5)
#    sched.add_job(my_job, 'cron', second='*/5', args = [CT.CONF_DIR + 'trader/ht.json'])
#    #sched.add_job(my_job, 'cron', minute = 10, hour = 13, args = [CT.CONF_DIR + 'trader/ht.json'])
    add_job(sched)
    sched.start()
    return

if __name__ == "__main__":
    main(sys.argv)
