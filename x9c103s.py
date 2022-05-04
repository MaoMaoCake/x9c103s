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
    def __init__(self, CS, INC, UD):
        self.CS = machine.Pin(CS, machine.OUT)
        self.INC = machine.Pin(INC, machine.OUT)
        self.UD = machine.Pin(UD, machine.OUT)
        self.sleep_time = 0.05
        self.cleanup()

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
        self.INC.off()
        time.sleep(self.sleep_time)

    def down(self):
        self.INC.on()
        self.UD.off()
        self.CS.off()
        time.sleep(0.1)
        self.INC.off()

    def store_value(self):
        self.INC.on()
        self.CS.on()
        time.sleep(0.1)
        self.CS.off()

    def read_value(self):
        pass

    def reset(self):
        self.INC.off()
        self.CS.on()
        time.sleep(0.1)
        self.CS.off()