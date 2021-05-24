# Escribe tu código aquí :-)
import time
from utime import ticks_add
from utime import ticks_diff
from machine import Pin
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


def Stepper_constant_speed(stepper, speed, time=1):
    """
    :param stepper: stepper to use
    :param speed: time to wait between steps
    :param time: time it will be moving in seconds
    """
    stepper.steps(time / (2 * stepper.step_time))

Step_angle = 1.8
####
#General parameters
Number_of_experiments = 1
Number_of_cleaning_cycles = 5
Experiment_Duration_in_minutes = 4 # Only integrers
Cleaning_cycle_duration_in_seconds = 10
Stirring_rate_rpm = 150 ### do not put rpm higer than 150
#############################################################
Tanto_por_uno_vuelta = Step_angle / 360
delay_in_minutes = (Tanto_por_uno_vuelta / 2) / Stirring_rate_rpm
delay_in_seconds = delay_in_minutes * 60
delay_in_microseconds = delay_in_seconds * 1000000
Number_of_experiments_Corrected = Number_of_experiments - 1

Stepper_Syringe_Pump = Precision_Stepper(step_pin=32, dir_pin=5, en_pin=33, step_time=1000)
Stepper_Autosampler = Precision_Stepper(step_pin=2, dir_pin=4, en_pin=15, step_time=1)
Steppers_Stirring = Precision_Stepper(step_pin=19, dir_pin=21, en_pin=18, step_time=1000)
Pump = Peristaltic_Pump(pin=26) #18
Valve_Cathode = Valve(pin=27)
Valve_Anode = Valve(pin=13)

Stepper_Syringe_Pump.power_off()
Stepper_Autosampler.power_off()

Steppers_Stirring.power_on()
Steppers_Stirring.set_dir(1)
deadline = ticks_add(time.ticks_ms(), 1000 * 5)
while ticks_diff(deadline, time.ticks_ms()) > 0:
    Steppers_Stirring.steps(1)
Steppers_Stirring.power_off()



