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


Stepper_Syringe_Pump = Precision_Stepper(step_pin=2, dir_pin=15, en_pin=4, step_time=1000)
Stepper_Autosampler = Precision_Stepper(step_pin=19, dir_pin=21, en_pin=5, step_time=1)
Steppers_Stirring = Precision_Stepper(step_pin=14, dir_pin=27, en_pin=26, step_time=1000)
Pump = Peristaltic_Pump(pin=18)
Valve_Cathode = Valve(pin=12)
Valve_Anode = Valve(pin=13)


#Electronics Parameters
Microstepping = 32
Standard_Step_Angle = 1.8
Pich_in_mm = 8
Full_rev = 360
Relation = (360 / 1.8) / 8

#General parameters
Number_of_experiments = 2
Number_of_cleaning_cycles = 1
Experiment_Duration_in_minutes = 1 # Only integrers
Cleaning_cycle_duration_in_seconds = 1
Stirring_rate_rpm = 100 ### do not put rpm higer than X


Stepper_Syringe_Pump.power_off()
Stepper_Autosampler.power_off()
Steppers_Stirring.power_off()

coordenades_mm = [00, 20, 40, 60, 80, 100, 156, 176, 196, 216, 236, 256]
coordenades_residus = 128

#Initial system conditioning sequence

#Move autosampler from vial 1 to residues
Stepper_Autosampler.power_on()
Stepper_Autosampler.set_dir(1)
Stepper_Autosampler.mm(abs(coordenades_residus), Relation * Microstepping)
Stepper_Autosampler.power_off()

#Fill cleaning water tubes
Pump.engage()
time.sleep_ms(1) #7500
Pump.disengage()

#Remove excess of water
Valve_Cathode.engage()
time.sleep_ms(1) #15000
Valve_Cathode.disengage()
Valve_Anode.engage()
time.sleep_ms(1) #15000
Valve_Anode.disengage()

#Fill injection pump tubes
Stepper_Syringe_Pump.power_on()
Stepper_Syringe_Pump.set_dir(0)
Stepper_Syringe_Pump.steps(1) # 18000 standard value
Stepper_Syringe_Pump.power_off()

#Remove excess of reactive
Valve_Cathode.engage()
time.sleep_ms(1) #15000
Valve_Cathode.disengage()
Valve_Anode.engage()
time.sleep_ms(1) #15000
Valve_Anode.disengage()

#Move autosampler from residues to vial 1
Stepper_Autosampler.power_on()
Stepper_Autosampler.set_dir(0)
Stepper_Autosampler.mm(abs(coordenades_residus), Relation * Microstepping)
Stepper_Autosampler.power_off()

#Set of experiments
for index_vial in range(Number_of_experiments):

    # REACCIO (Sequencia de codi de tota la reacció)

    Stepper_Syringe_Pump.power_on()
    Stepper_Syringe_Pump.set_dir(0)
    Stepper_Syringe_Pump.steps(9000)
    Stepper_Syringe_Pump.power_off()

    Start = str(input(""))
    Start = str(input("System is set up, Are you ready? "))

    print("Experiment will start in 5 seconds, power on the potentiostat")
    time.sleep_ms(5000)
    print("Experiment " + str(index_vial + 1) + " started")

    Steppers_Stirring.power_on()
    Steppers_Stirring.set_dir(1)
    deadline = ticks_add(time.ticks_ms(), 1000 * 60 * Experiment_Duration_in_minutes)
    while ticks_diff(deadline, time.ticks_ms()) > 0:
        Steppers_Stirring.steps(1)
    Steppers_Stirring.power_off()

    print("Experiment ended store your data")

    Valve_Cathode.engage()
    time.sleep_ms(15000)
    Valve_Cathode.disengage()
    Valve_Anode.engage()
    time.sleep_ms(15000)
    Valve_Anode.disengage()

    travel = coordenades_residus - coordenades_mm[index_vial]

    if travel > 0:
        Stepper_Autosampler.set_dir(1)
    else:
        Stepper_Autosampler.set_dir(0)

    Stepper_Autosampler.power_on()
    Stepper_Autosampler.mm(abs(travel), Relation * Microstepping)
    Stepper_Autosampler.power_off()

    print("Cleaning started")

    # LLIMPIAT (Codi del Limpiat)

    for cleaning_batches in range(Number_of_cleaning_cycles):

        Pump.engage()
        time.sleep_ms(8000)
        Pump.disengage()

        Steppers_Stirring.power_on()
        Steppers_Stirring.set_dir(1)
        deadline = ticks_add(time.ticks_ms(), 1000 * Cleaning_cycle_duration_in_seconds)
        while ticks_diff(deadline, time.ticks_ms()) > 0:
            Steppers_Stirring.steps(1)
        Steppers_Stirring.power_off()

        Valve_Cathode.engage()
        time.sleep_ms(15000)
        Valve_Cathode.disengage()
        Valve_Anode.engage()
        time.sleep_ms(15000)
        Valve_Anode.disengage()

        print("Cleaning batch " + str(cleaning_batches + 1) + " done")

    travel = coordenades_residus - coordenades_mm[index_vial + 1]

    if travel > 0:
        Stepper_Autosampler.set_dir(0)
    else:
        Stepper_Autosampler.set_dir(1)

    Stepper_Autosampler.power_on()
    Stepper_Autosampler.mm(abs(travel), Relation * Microstepping)
    Stepper_Autosampler.power_off()

    print("Cleaning Ended, do you want to start next experiment? (wait few seconds for injection pump to finish)")

print("All experiments ended")
