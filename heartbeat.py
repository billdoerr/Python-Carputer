# !/usr/bin/python3

"""
    heartbeat.py

    Blinks LED on/off indicating that the RPi is still running.

"""

__version__ = '1.0'
__author__ = 'Bill Doerr'


import RPi.GPIO as GPIO
from time import sleep


# Define some constants
CHANNEL = 13        # Pinout #13, GPIO #27
HEARTBEAT = 0.5     # Value in seconds


# GPIO initialization
def gpio_init():
    # Using RPi pin out.  GPIO Pin #37.  Button connected to GPIO -> Pin #37 and GND -> Pin #38
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(CHANNEL, GPIO.OUT)


def main():

    gpio_init()

    try:
        # Loop while computer's power is on
        while True:
            GPIO.output(CHANNEL, GPIO.HIGH)
            sleep(HEARTBEAT)
            GPIO.output(CHANNEL, GPIO.LOW)
            sleep(HEARTBEAT)

    except KeyboardInterrupt:
        pass

    except:
        # This catches ALL other exceptions including errors.
        # You won't get any error messages for debugging
        # so only use it once your code is working.
        pass

    finally:
        GPIO.output(CHANNEL, GPIO.LOW)
        GPIO.cleanup()  # This ensures a clean exit.  Enables all pins for INPUT, but only for this program.


if __name__ == "__main__":
    main()
