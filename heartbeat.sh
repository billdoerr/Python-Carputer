#! /bin/sh

# heartbeat

### BEGIN INIT INFO
# Provides:          listen_for_shutdown.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting heartbeat.py..."
    python3 /usr/local/bin/heartbeat.py &
    ;;
  stop)
    echo "Stopping heartbeat.py..."
    pkill -f /usr/local/bin/heartbeat.py
    ;;
    restart)
    echo "Restarting heartbeat.py..."
    stop
    start
    ;;
    status)
    echo "Status heartbeat.py..."
    PID=`pgrep -f /usr/local/bin/heartbeat.py`
    ps ${PID}
    ;;
  *)
    echo "Usage: /etc/init.d/heartbeat.sh {start|stop|status|restart}"
    exit 1
    ;;
esac

exit 0

