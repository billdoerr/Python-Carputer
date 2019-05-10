# !/usr/bin/python3

"""
    listen_for_shutdown.py

    Listens for button press on GPIO pin.

    After being depressed for ~5 seconds will send shutdown command
    to Ip's listed in the dnsmasq.leases file.  When this completes
    shutdown command will be sent to the node hosting this script.

    https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi
    https://www.daniweb.com/programming/software-development/threads/507019/python-program-to-extract-ip-addresses-from-a-log-file
"""

__version__ = '1.0'
__author__ = 'Bill Doerr'


import RPi.GPIO as GPIO
import subprocess
import paramiko
import re
from time import sleep
import datetime
import logging


# Define some constants
CHANNEL = 26   # Pinout #37, GPIO #26
TIMEOUT = 20
BUTTON_PRESSED_TIME = 3   # Amount of time button must be pressed


# Log file initialization
def log_init():
    global logger
    # Set up logging to file
    logging.basicConfig(
        filename='/var/log/carputer/listen_for_shutdown.log',
        level=logging.INFO,
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # Set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # Set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    # Add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logger = logging.getLogger(__name__)

    logger.info("Logging initialized.")


# GPIO initialization
def gpio_init():
    # Using RPi pin out.  GPIO Pin #37.  Button connected to GPIO -> Pin #37 and GND -> Pin #38
    # GPIO.setmode(GPIO.BOARD)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.wait_for_edge(CHANNEL, GPIO.FALLING)
    GPIO.add_event_detect(CHANNEL, GPIO.FALLING, callback=button_press_callback, bouncetime=200)

    logger.info("GPIO initialized.")


# Parses Ip's from dns lease file
def get_nodes():
    filename = '/var/lib/misc/dnsmasq.leases'
    # filename = '/home/pi/python/dnsmasq.leases'
    nodes = []
    try:
        leasefile = list(open(filename, 'r').read().split('\n'))
        logger.info("Lease file opened:  " + str(leasefile))
        for entry in leasefile:
            ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', entry)
            for ip in ips:
                logger.info("Ip added to nodes:  " + ip)
                nodes.append(ip)
    except IOError:
        logger.error("Unable to open file:  " + filename)
    finally:
        if nodes:   # empty sequences are false
            logger.info("Nodes returned:  " + str(nodes))
            return nodes
        else:
            logger.info("Nodes returned:  None")
            return None


# Sends shutdown command to specified ip
def shutdown_node(ip):
    ssh = paramiko.SSHClient()
    isconnected = False
    try:
        # Sure ain't very secure
        ssh.connect(ip, username='pi', password='scoobydoo', timeout=TIMEOUT)
        isconnected = True
    except:
        logger.info("SSH connection error.")

    if isconnected:
        try:
            # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo shutdown -h now', timeout=TIMEOUT)
            ssh.exec_command('sudo shutdown -h now', timeout=TIMEOUT)
        except:
            logger.info("SSH shutdown nodes error.")


# Loop through nodes and perform shutdown command
def shutdown_nodes():
    # Loop through nodes and send shutdown
    nodes = get_nodes()
    for node in nodes:
        logger.info("Shutting down node: " + str(node))
        shutdown_node(node)


# Button press callback
def button_press_callback(channel):
    logger.info("button_press_callback")

    # Removes event detection for a pin.
    GPIO.remove_event_detect(channel)

    logger.info('Button pressed')

    pressed_time_start = datetime.datetime.now()

    while not GPIO.input(channel):
        pressed_time_total = (datetime.datetime.now() - pressed_time_start).seconds

        # Must hold button down for period of time
        if pressed_time_total > BUTTON_PRESSED_TIME:
            logger.info("Shutting down nodes.")
            # Shutdown slave nodes
            shutdown_nodes()
            # Shutdown master node
            logger.info("Shutting down master node.")
            subprocess.call(['sudo', 'shutdown', '-h', 'now'], shell=False)
        else:
            logger.info("Button was not pressed long enough to perform shutdown.")

    # Re-enable callback if button press too short or shutdown failed for some reason
    GPIO.add_event_detect(CHANNEL, GPIO.FALLING, callback=button_press_callback, bouncetime=200)


def main():

    log_init()
    gpio_init()

    try:
        # Loop until shutdown
        logger.info("Starting main loop.")
        while True:
            sleep(1)

    except KeyboardInterrupt:
        logger.error("Keyboard interrupt.")

    except:
        # This catches ALL other exceptions including errors.
        # You won't get any error messages for debugging
        # so only use it once your code is working.
        logger.error("Unknown exception.")

    finally:
        logger.info("Performing GPIO cleanup.")
        GPIO.cleanup()  # This ensures a clean exit.  Enables all pins for INPUT, but only for this program.


if __name__ == "__main__":
    main()

