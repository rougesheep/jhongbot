#!/usr/bin/env bash

case "$1" in:
    "start":
        start()
        ;;
    "stop":
        stop()
        ;;
    "restart":
        stop()
        start()
        ;;
    default:
        echo "Usage: ./wrapper.sh <start|stop|restart>"
        ;;
esac

function start {
    . ./venv/bin/activate
    nohup python3.7 -u wishingwall.py > python.log 2>&1 &
    echo $! > python.pid
}

function stop {
    kill $(cat python.pid) && rm -f python.pid
}