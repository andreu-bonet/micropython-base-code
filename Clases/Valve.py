import time
from utime import ticks_add
from utime import ticks_diff
from machine import Pin
from time import sleep_us

class Valve:
    """Class for opening and closing valves"""

    def __init__(self, pin):
        """Initialise valve."""
        self.pin = pin
        self.pin = Pin(pin, Pin.OUT)
        self.disengage()

    def engage(self):
        """Power on valve."""
        self.pin.value(1)

    def disengage(self):
        """Power off valve."""
        self.pin.value(0)

    def status(self):
        """Return status of the valve. 0 disengaged - 1 engaged"""
        return self.pin.value
