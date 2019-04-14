#!/usr/bin/env bash
. ./venv/bin/activate
nohup python3.7 -u wishingwall.py > python.log 2>&1 &
echo $! > python.pid