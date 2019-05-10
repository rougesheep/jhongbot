#!/usr/bin/env bash

function start {
    . ./venv/bin/activate
    python3.7 -u wishingwall.py
    # nohup python3.7 -u wishingwall.py > python.log 2>&1 &
    # echo $! > python.pid
}

function stop {
    kill $(cat python.pid) && rm -f python.pid
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage: ./wrapper.sh <start|stop|restart>"
        exit 1
        ;;
esac