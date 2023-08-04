from environment import getEnvValue
from machine import Pin
from time import sleep

# Config Parameters
gpionr = int(getEnvValue("gpionr"))

# init stuff (default high)
pin = Pin(gpionr, Pin.OUT)
pin.high()


def triggerUnlock():
    print(f"Triggering the opening of the lock by setting Pin {gpionr} low.")
    pin.low()
    sleep(0.2)
    pin.high()