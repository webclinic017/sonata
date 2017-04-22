#!/bin/sh
#****************************************************************#
# ScriptName: get_tick.sh
# Author: www.zhangyunsheng.com@gmail.com
# Create Date: 2016-04-10 17:39
# Modify Date: 2016-04-13 04:00
# Copyright ? 2016 Renren Incorporated. All rights reserved.
#***************************************************************#

THRD_CNT=10

function help() {
    echo 'sh get_tick.sh tick 000001 2016-04-08'
    echo 'sh get_tick.sh since 000001 2016-04-08'
    echo 'sh get_tick.sh symbol 000001'
    echo 'sh get_tick.sh date 2016-04-08'
    echo 'sh get_tick.sh allsince 2016-04-08'
}

if [ $# -eq 0 ]
then
    help
    exit -1
fi
if [ $# -gt 0 ]
then
    if [ X$1 = X'-h' ]
    then
        help
        exit
    fi
fi


if [ $1 == 'tick' ]
then
    python get_tick.py -m tick -s $2 -a $3
elif [ $1 == 'since' ]
then
    for((i=0; i<$THRD_CNT; ++i))
    do
        python get_tick.py -m since -s $2 -a $3 -i $i -t $THRD_CNT &
    done
elif [ $1 == 'symbol' ]
then
    for((i=0; i<$THRD_CNT; ++i))
    do
        python get_tick.py -m symbol -s $2 -i $i -t $THRD_CNT &
    done
elif [ $1 == 'date' ]
then
    for((i=0; i<$THRD_CNT; ++i))
    do
        python get_tick.py -m date -a $2 -i $i -t $THRD_CNT &
    done
elif [ $1 == 'allsince' ]
then
    for((i=0; i<$THRD_CNT; ++i))
    do
        python get_tick.py -m allsince -a $2 -i $i -t $THRD_CNT &
    done
else
    help
fi
