#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import datetime
import time

def check_dir(dir):
    """
    检查目录是否存在，如果不存在则创建
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
    return True

def check_file_expired(file, expire):
    """
    检查文档是否过期
    --------
    file: 文件路径
    expire：过期时间(分)
    """
    if not os.path.exists(file):
        return True
    statinfo = os.stat(file)
    mtime = statinfo.st_mtime
    now = time.time()
    if (now - mtime)/60 > expire:
        return True
    else:
        return False

def main(argv):
    #import const as CT
    #check_dir(CT.TICK_DIR + 'sh000001/1991-01-01')
    return

if __name__ == "__main__":
    main(sys.argv)
