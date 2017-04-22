#!/bin/sh
#****************************************************************#
# ScriptName: get_history.sh
# Author: www.zhangyunsheng.com@gmail.com
# Create Date: 2016-04-10 17:39
# Modify Date: 2016-04-13 02:12
# Copyright ? 2016 Renren Incorporated. All rights reserved.
#***************************************************************#

THRD_CNT=100

function help() {
    echo 'sh get_history.sh #取所有股票的历史数据'
    echo 'sh get_history.sh 000001 #获取指定股票历史数据'
}

if [ $# -gt 0 ]
then
    if [ X$1 = X'-h' ]
    then
        help
        exit
    fi
fi


if [ $# -eq 0 ]
then
    #获取所有股票的历史数据
    for((i=0; i<$THRD_CNT; ++i))
    do
        python get_history.py -m all -i $i -t $THRD_CNT &
    done
elif [ $# -eq 1 ]
then
    #获取指定股票历史数据
    python get_history.py -m symbol -s $1
else
    help
fi
