#!/bin/sh

PY='python3'
BIN='quant/quant.py'

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
      ${PY} $root"/$BIN" 2>&1 | awk '{print "["strftime("%F %H:%M:%S")"]"$0}' >>$root"/log/out.log" &
    elif [ $os == "Mac" ];then
      ${PY} $root"/$BIN" 2>&1 | awk '{system("date"); print}' >>$root"/log/out.log" &
    fi
    #${PY} $root"/quant/quant.py" >>$root"/log/out.log" 2>&1 &

    #$bin"/daemontools/command/supervise" $bin >>$root"/log/supervise.log" 2>&1 &
    RET=$?
    exit $RET
    ;;
  stop)
    echo "stop"
    if [ $os == "Linux" ];then
      ps elx | grep "$BIN" | grep -v "grep" | awk '{printf "%s %s\n",$3,$10;}' > npipe
    elif [ $os == "Mac" ];then
      ps elx | grep "$BIN" | grep -v "grep" | awk '{printf "%s %s\n",$2,$11;}' > npipe
    fi
    while read pid_now_item
    do
      arr=($pid_now_item)
      pid_now=${arr[0]}
      pstatus=${arr[1]}
      if [ ! -e $pid_now ];then
        pid=$pid_now
        if [ 'S' == $pstatus ] || [ 'R' == $pstatus ];then
          kill -TERM $pid
          echo "kill -SIGTERM $BIN pid:$pid"
        else
          kill -KILL $pid
          echo "kill -KILL $BIN pid:$pid"
        fi
      else
        echo "no $BIN to kill\n"
      fi
    done < npipe
    rm -rf npipe;
    ;;
  view)
    ps aux | grep "$BIN" | grep -v "grep"
    ;;
esac
