# Escribe tu código aquí :-)
# Escribe tu código aquí :-)
from machine import Pin
import time
from time import sleep_us


class Precision_Stepper:
    """Class for stepper motor"""

    def __init__(self, step_pin, dir_pin, en_pin, step_time=1000, steps_per_rev=1600):
        """Initialise stepper."""
        self.stp = Pin(step_pin, Pin.OUT)
        self.dir = Pin(dir_pin, Pin.OUT)
        self.en = Pin(en_pin, Pin.OUT, value=0)

        self.step_time = step_time  # us
        self.steps_per_rev = steps_per_rev

    def power_on(self):
        """Power on stepper."""
        self.en.value(0)

    def power_off(self):
        """Power off stepper."""
        self.en.value(1)

    def set_dir(self, _dir):
        self.dir.value(_dir)

    def steps(self, step_count):
        """Rotate stepper for given steps."""
        for i in range(abs(step_count)):
            self.stp.value(1)
            sleep_us(self.step_time)
            self.stp.value(0)
            sleep_us(self.step_time)

    def mm(self, mm, step_per_mm):
        self.steps(mm * step_per_mm)

    def set_step_time(self, us):
        """Set time in microseconds between each step."""
        self.step_time = us


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


class Peristaltic_Pump:
    """Class for start and stop Gilson Peristaltic_Pump"""

    def __init__(self, pin):
        """Initialise Pump."""
        self.pin = pin
        self.pin = Pin(pin, Pin.OUT)
        self.disengage()

    def engage(self):
        """Power on valve."""
        self.pin.value(0)

    def disengage(self):
        """Power off valve."""
        self.pin.value(1)

    def status(self):
        """Return status of the valve. 0 disengaged - 1 engaged"""
        return self.pin.value


Stepper_Syringe_Pump = Precision_Stepper(step_pin=32, dir_pin=5, en_pin=33, step_time=1000)
Stepper_Autosampler = Precision_Stepper(step_pin=2, dir_pin=4, en_pin=15, step_time=1000)
Steppers_Stirring = Precision_Stepper(step_pin=19, dir_pin=21, en_pin=18, step_time=1000)
Pump = Peristaltic_Pump(pin=26) #18
Valve_Cathode = Valve(pin=27)
Valve_Anode = Valve(pin=13)

Microstepping = 32
Standard_Step_Angle = 1.8
Pich_in_mm = 8
Full_rev = 360
Relation = (360 / 1.8) / 8

Stepper_Syringe_Pump.power_off()
Stepper_Autosampler.power_off()
Steppers_Stirring.power_off()

Pump.engage()
Pump.disengage()

Valve_Cathode.disengage()
Valve_Anode.disengage()
