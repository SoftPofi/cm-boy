#!/bin/bash
echo "Start cron job"
echo "Remove running screen sessions"
screen -ls | grep '(Detached)' | awk '{print $1}' | xargs -I % -t screen -X -S % quit
echo "Run CmLeash in screen"
screen -L -Logfile ./log/screen.log -dm bash -c 'cd $cm_base_dir; git checkout main; git pull; python3 CmLeash.py -f -o'
echo "Done"