#!/bin/bash
echo "Start cron job"
screen -ls | grep '(Detached)' | awk '{print $1}' | xargs -I % -t screen -X -S % quit
screen -dm bash -c 'python3 CmLeash.py -f -o'