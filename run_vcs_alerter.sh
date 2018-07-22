#!/bin/bash

export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/local/lib
export PYTHONPATH=/home/ubuntu/Code/vcs-alerter/
cd /home/ubuntu/Code/vcs-alerter/server
nohup python3 __init__.py &