#!/usr/bin/env bash

cd "$(dirname "$0")"

function start {
    . ./venv/bin/activate
    nohup python -u jhongbot.py > python.log 2>&1 &
    echo $! > python.pid
}

function stop {
    kill $(cat python.pid) && rm -f python.pid
}

function foreground {
    . ./venv/bin/activate
    python -u jhongbot.py
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
