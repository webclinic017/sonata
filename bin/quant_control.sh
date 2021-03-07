#!/bin/sh

PY='python3'

os='Linux'
if [ "$(uname)" == "Darwin" ];then
    os='Mac'
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ];then
    os='Linux'
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ];then
    os='Windows'
fi

#bin=`dirname $(readlink -f $0)`
bin=`dirname $0`
root=$bin"/../"

INTERFACE=$1
shift

case "$INTERFACE" in
    start)
        START_PARA=$*
        echo "start"

        if [ $os == "Linux" ];then
            ${PY} $root"/quant/quant.py" 2>&1 | awk '{print "["strftime("%F %H:%M:%S")"]"$0}' >>$root"/log/out.log" &
        elif [ $os == "Mac" ];then
            ${PY} $root"/quant/quant.py" 2>&1 | awk '{system("date"); print}' >>$root"/log/out.log" &
        fi
        #${PY} $root"/quant/quant.py" >>$root"/log/out.log" 2>&1 &

        #$bin"/daemontools/command/supervise" $bin >>$root"/log/supervise.log" 2>&1 &
        RET=$?
        exit $RET
        ;;
esac
