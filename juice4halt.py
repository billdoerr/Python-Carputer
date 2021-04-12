# !/usr/bin/python3

"""
    juice4halt.py

    This is copied from listen_for_shutdown.py, which may be obsoleted in the future.
    The function 'button_press_callback' has been commented out along with references
    in the 'gpio_init' function.

    Flashes Yellow LED to indicate RPi is shutting down.

    https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi
    https://www.daniweb.com/programming/software-development/threads/507019/python-program-to-extract-ip-addresses-from-a-log-file
"""

__version__ = '1.0'
__author__ = 'Bill Doerr'
__date__ = '18Apr2021'


import RPi.GPIO as GPIO
import subprocess
import paramiko
import re
from time import sleep
import datetime
import logging
import threading


# Define some constants
CHANNEL_LED = 13            # Pinout #33, GPIO 13
TIMEOUT = 20                # Value in seconds
DELAY_SLOW = 0.25           # Value in seconds
DELAY_FAST = 0.1            # Value in seconds


# Log file initialization
def log_init():
    global logger

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s:%(levelname)s:\t%(message)s', '%H:%M:%S')

    file_handler = logging.FileHandler('/var/log/carputer/juice4halt.log', 'w')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    # logging.getLogger('').addHandler(console)
    logger.addHandler(console)

    logger.info("Logging initialized.")


# GPIO initialization
def gpio_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHANNEL_LED, GPIO.OUT)

    logger.info("GPIO initialized.")


# Parses Ip's from dns lease file
def get_nodes():
    # filename = '/var/lib/misc/dnsmasq.leases'
    filename = '/etc/carputer/nodes.config'
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
            logger.info("SSH shutdown node error.")


# Loop through nodes and perform shutdown command
def shutdown_nodes():
    # Loop through nodes and send shutdown
    nodes = get_nodes()
    for node in nodes:
        logger.info("Shutting down node: " + str(node))
        shutdown_node(node)


# LED indicator that power off button pressed
def flash_led(e, mode):
    while not e.isSet():
        if mode == 1:   # Slow
            GPIO.output(CHANNEL_LED, GPIO.HIGH)
            sleep(DELAY_SLOW)
            GPIO.output(CHANNEL_LED, GPIO.LOW)
            sleep(DELAY_SLOW)
        elif mode == 2:     # Fast
            GPIO.output(CHANNEL_LED, GPIO.HIGH)
            sleep(DELAY_FAST)
            GPIO.output(CHANNEL_LED, GPIO.LOW)
            sleep(DELAY_FAST)

def led_flash():
    # Indicate we are shutting down
    e = threading.Event()
    logger.info("Indicate we are shutting down.")
    t = threading.Thread(name='non-block', target=flash_led, args=(e, 2))
    t.start()   # Start faster LED flashing

def main():

    log_init()
    gpio_init()
    
    # Indicate we are shutting down
    logger.info("Indicate we are shutting down.")
    led_flash()

    # Shutdown slave nodes
    logger.info("Shutting down slave nodes.")
    shutdown_nodes()
    # Shutdown master node
    logger.info("Shutting down master node.")
    subprocess.call(['sudo', 'shutdown', '-h', 'now'], shell=False)

    logger.info("Performing GPIO cleanup.")
    GPIO.output(CHANNEL_LED, GPIO.LOW)
    GPIO.cleanup()  # This ensures a clean exit.  Enables all pins for INPUT, but only for this program.


if __name__ == "__main__":
    main()
