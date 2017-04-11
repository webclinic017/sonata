#!/bin/sh
#****************************************************************#
# @Brief: quant_control.sh
# @Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2017-04-06 01:22
# @ModifyDate: 2017-04-11 13:17
# Copyright ? 2017 Baidu Incorporated. All rights reserved.
#***************************************************************#

bin=`dirname $(readlink -f $0)`
root=$bin"/../"

INTERFACE=$1
shift

case "$INTERFACE" in
    start)
        START_PARA=$*
        echo "start"
        python $root"/quant/quant.py" >>$root"/log/out.log" 2>&1 &
        RET=$?
        exit $RET
        ;;
esac
