from environment import getEnvValue
from machine import Pin
from time import sleep

# Config Parameters
gpionr = int(getEnvValue("gpionr"))

# init stuff (default high)
pin = Pin(gpionr, Pin.OUT)
pin.low()


def triggerUnlock():
    print(f"Triggering the opening of the lock by setting Pin {gpionr} high.")
    pin.high()
    sleep(0.2)
    pin.low()