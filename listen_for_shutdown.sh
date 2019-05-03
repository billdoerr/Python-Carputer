#! /bin/sh

# listen_for_shutdown.sh

# https://werxltd.com/wp/2012/01/05/simple-init-d-script-template/
# https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi

### BEGIN INIT INFO
# Provides:          listen_for_shutdown.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting listen_for_shutdown.py..."
    python3 /usr/local/bin/listen_for_shutdown.py &
    ;;
  stop)
    echo "Stopping listen_for_shutdown.py..."
    pkill -f /usr/local/bin/listen_for_shutdown.py
    ;;
    restart)
    echo "Restarting listen_for_shutdown.py..."
    stop
    start
    ;;
    status)
    echo "Status listen_for_shutdown.py..."
    PID=`pgrep -f /usr/local/bin/listen_for_shutdown.py`
    ps ${PID}
    ;;
  *)
    echo "Usage: /etc/init.d/listen_for_shutdown.sh {start|stop|status|restart}"
    exit 1
    ;;
esac

exit 0

