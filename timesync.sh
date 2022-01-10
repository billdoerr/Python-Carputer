#! /bin/sh

# /bin/timesync.sh
# v1.1.1 9Jan2022

master_up=0
sh -c 'echo "Waiting for master node..." >> /tmp/timesync.log'
while [ $master_up -ne 1 ]; do
    ping -c 1 192.168.4.1
        if [ $? -eq  0 ]; then
            sh -c 'echo "Master node online!" >> /tmp/timesync.log'
            # Get date from master node and set date
            sh -c 'echo "Time sync ->" >> /tmp/timesync.log'
            # sudo apt-get install sshpass
            sudo date -s "`sshpass -p 'scoobydoo' ssh pi@192.168.4.1 'date'`" >> /tmp/timesync.log
            master_up=1;
        else
            sh -c 'echo -n "."  >> /tmp/timesync.log'
    fi
done
