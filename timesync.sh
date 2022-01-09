#! /bin/sh

# /bin/timesync.sh
# v1.1 24Dec2021

# LOG_FILE=/var/log/timesync.log  # For debugging
LOG_FILE=/tmp/timesync.log    # New file each reboot
MASTER_UP=0
sh -c 'echo "Waiting for master node..." >> LOG_FILE'
while [ $MASTER_UP -ne 1 ]; do
    ping -c 1 192.168.4.1
        if [ $? -eq  0 ]; then
            sh -c 'echo -e "\nMaster node online!" >> LOG_FILE'
            # Get date from master node and set date
            sh -c 'echo "Time sync ->" >> LOG_FILE'
            date -s "`sshpass -p 'scoobydoo' ssh pi@192.168.4.1 'date'`" >> LOG_FILE
            MASTER_UP=1;
        else
            sh -c 'echo -n "."  >> LOG_FILE'
    fi
done