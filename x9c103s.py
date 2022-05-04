# The MIT License (MIT)
# Copyright (c) 2022 Jirapong Pansak
# https://opensource.org/licenses/MIT

# Platform-specific MicroPython code for the x9c103s Voltage controlled Resistor.
# This code is made with reference to the x9c103s datasheet.
# Documentation:
#   https://github.com/MaoMaoCake/x9c103s

import time
import machine


class x9c103s:
    def __init__(self, CS, INC, UD, soft_store=False, sleep_time=0.05):
        self.CS = machine.Pin(CS, machine.Pin.OUT)
        self.INC = machine.Pin(INC, machine.Pin.OUT)
        self.UD = machine.Pin(UD, machine.Pin.OUT)
        self.sleep_time = sleep_time
        self.INC.on()
        self.UD.on()
        self.value = False
        # soft store is a workaround for the chip as it cannot report its own value
        # therefore, the value must be stored by the driver class
        # in order to be able to report the value the driver will ramp
        # down to value of 0
        self.soft_store = soft_store
        if self.soft_store:
            print("WARNING: x9c103s Soft storage enabled, This can cause issues if your code depends on having the true value of the resistor")
            print("The Driver class will not be able to report the true value if any of the following are true:")
            print("- The chip Loses connection to the driver class While changing the value")
            print("- The Driver class is replaced without first calling ramp_0()")
            self.ramp_0()
            self.value = 0

    # forces the chip to step down 100 times
    # the chip has 100 steps and is unable to
    # report on the current step number
    # therefore, the only way to know the current step
    # number is to step down to 0
    # this is a workaround for the chip as its resistance
    # steps do not wrap
    def ramp_0(self):
        for i in range(100):
            self.down()

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        self.CS.off()
        self.INC.off()
        self.UD.off()

    def up(self):
        self.CS.off()
        self.UD.on()
        time.sleep(self.sleep_time)
        self.INC.off()
        time.sleep(self.sleep_time)
        self.INC.on()
        time.sleep(self.sleep_time)
        if self.soft_store:
            self.value += 1

    def down(self):
        self.CS.off()
        self.UD.off()
        time.sleep(self.sleep_time)
        self.INC.off()
        time.sleep(self.sleep_time)
        self.INC.on()
        time.sleep(self.sleep_time)
        if self.soft_store:
            self.value -= 1

    # sets the built-in memory to the value of the resistor currently set
    def store_value(self):
        self.INC.on()
        self.CS.on()
        time.sleep(0.1)
        self.CS.off()

    # this is not supported by the chip
    def get_value(self):
        if self.soft_store:
            return self.value
        else:
            print("ERROR: x9c103s.read_value() is not supported by the chip unless soft_store is enabled")
            print("Please enable soft_store in the constructor soft_store=True")
            print("This will allow the driver class to store the value of the resistor")

    def set_value(self, value):
        if self.soft_store:
            if value > self.value:
                for i in range(value - self.value):
                    self.up()
            elif value < self.value:
                for i in range(self.value - value):
                    self.down()
        else:
            print("ERROR: x9c103s.set_value() is not supported by the chip unless soft_store is enabled")
            print("Please enable soft_store in the constructor soft_store=True")
            print("This will allow the driver class to store the value of the resistor")

    # WIP - not working
    def reset(self):
        self.INC.off()
        self.CS.on()
        time.sleep(0.1)
        self.CS.off()