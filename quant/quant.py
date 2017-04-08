#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: quant.py
# @Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-05-19 00:46
# @ModifyDate: 2016-05-19 00:46
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import os
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from trader.trader import Trader
import utils.const as CT
import yaml
import logging
import logging.config
from strategy import *


def execute(job):

    job['contex'] = {}
    job['contex']['status'] = 1
    job['contex']['result'] = []
    if 'portfolio' in job.keys() and job['portfolio'] != None:
        portfolio = yaml.load(file(CT.CONF_DIR + 'portfolio/' + job['portfolio']))
        job['contex']['result'] = portfolio

    for strategy in job['strategies']:
        if strategy['switch'] != 1:
            continue

        job['contex']['strategy'] = strategy
        obj = eval(strategy['name'])()
        obj.execute(job)

        #job终止
        if job['contex']['status'] == 0:
            break

    return 0

def add_job(scheduler, jobs):
    for job in jobs:
        if job['switch'] != 1:
            continue
        second = '*'
        minute = '*'
        hour = '*'
        day = '*'
        month = '*'
        year = '*'
        day_of_week = '*'

        cron = job['cron']
        second = cron['second'] if 'second' in cron else '*'
        minute = cron['minute'] if 'minute' in cron else '*'
        hour = cron['hour'] if 'hour' in cron else '*'
        day = cron['day'] if 'day' in cron else '*'
        month = cron['month'] if 'month' in cron else '*'
        year = cron['year'] if 'year' in cron else '*'
        day_of_week = cron['day_of_week'] if 'day_of_week' in cron else '*'

        scheduler.add_job(execute, 'cron', second=second, minute=minute, hour=hour, day=day, month=month, year=year, day_of_week=day_of_week, args = [job])

    return 0


def main(argv):
    #设置当前工作目录
    os.chdir(CT.HOME)
    logging.config.fileConfig(CT.CONF_DIR + "logger.conf")
    #logging.getLogger("warn").warning('This is warning message')

    jobstores = {'default':MemoryJobStore()}
    executors = {
        'default': ThreadPoolExecutor(10),
        #'processpool': ProcessPoolExecutor(3)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }

    scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    jobs = yaml.load(file(CT.CONF_DIR + 'jobs.yaml'))
    add_job(scheduler, jobs)
    scheduler.start()
    return

if __name__ == "__main__":
    main(sys.argv)
