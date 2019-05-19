#! /bin/sh

#
# /etc/init.d
# listen_for_shutdown.sh
#

# https://werxltd.com/wp/2012/01/05/simple-init-d-script-template/
# https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi

### BEGIN INIT INFO
# Provides:          listen_for_shutdown.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

start() {
    echo "Starting listen_for_shutdown.py..."
    # Remove log file upon start.  Used only for debugging.
    sudo rm -f /var/log/carputer/listen_for_shutdown.log
    python3 /usr/local/bin/listen_for_shutdown.py &
    return
}

stop() {
    echo "Stopping listen_for_shutdown.py..."
    pkill -f /usr/local/bin/listen_for_shutdown.py
    return
}

status() {
    echo "Status listen_for_shutdown.py..."
    PID=`pgrep -f /usr/local/bin/listen_for_shutdown.py`
    ps ${PID}
    return
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
  status)
        status
    ;;
  *)
        echo "Usage: /etc/init.d/listen_for_shutdown.sh {start|stop|status|restart}"
        exit 1
    ;;
esac

exit 0
