# Copyright (c) 2012 Calin Crisan <ccrisan@gmail.com>
#
# This file is part of PiLowLib.
#
# PiLowLib is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PiLowLib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PiLowLib.  If not, see <http://www.gnu.org/licenses/>.

'''Allows an easy configuration of the alternative functions
available for each of the GPIO pins of the RPi.
'''

import regs

# GPIO digital I/O
DIGITAL_IN = 0
DIGITAL_OUT = 1

# Broadcom Serial Control bus
SDA0 = 2
SCL0 = 3
SDA1 = 4
SCL1 = 5

# general purpose clocks
GPCLK0 = 6
GPCLK1 = 7
GPCLK2 = 8

# SPI
SPI0_CE0 = 9
SPI0_CE1 = 10
SPI0_MSIO = 11
SPI0_MOSI = 12
SPI0_SCLK = 13
SPI1_CE0 = 14
SPI1_CE1 = 15
SPI1_MSIO = 16
SPI1_MOSI = 17
SPI1_SCLK = 18
SPI2_CE0 = 19
SPI2_CE1 = 20
SPI2_CE2 = 21
SPI2_MSIO = 22
SPI2_MOSI = 23
SPI2_SCLK = 24

# PWM
PWM0 = 25
PWM1 = 26

# UART
TXD0 = 27
RXD0 = 28
CTS0 = 29
RTS0 = 30
TXD1 = 31
RXD1 = 32
CTS1 = 33
RTS1 = 34

# PCM
PCM_CLK = 35
PCM_FS = 36
PCM_DIN = 37
PCM_DOUT = 38

# secondary memory
SA0 = 39
SA1 = 40
SA2 = 41
SA3 = 42
SA4 = 43
SA5 = 44
SD0 = 45
SD1 = 46
SD2 = 47
SD3 = 48
SD4 = 49
SD5 = 50
SD6 = 51
SD7 = 52
SD8 = 53 
SD9 = 54
SD10 = 55
SD11 = 56
SD12 = 57
SD13 = 58
SD14 = 59
SD15 = 60
SD16 = 61
SD17 = 62
SOE_SE = 63
SWE_SRW = 64

# Broadcom Serial Control bus slave data / SPI slave
BSCSL_SDA_MOSI = 65
BSCSL_SCL_SCLK = 66
BSCSL_MSIO = 67
BSCSL_CE = 68

SD1_CLK = 69
SD1_CMD = 70
SD1_DAT0 = 71
SD1_DAT1 = 72
SD1_DAT2 = 73
SD1_DAT3 = 74

# JTAG
ARM_TRST = 75
ARM_RTCK = 76
ARM_TDO = 77
ARM_TCK = 78
ARM_TDI = 79
ARM_TMS = 80

MAX_FUNC = 80
MAX_GPIO = 53

# available functions for each of the GPIO pin
_functions = [
    (DIGITAL_IN, DIGITAL_OUT, SDA0, SA5, None, None, None, None), # GPIO PIN 0
    (DIGITAL_IN, DIGITAL_OUT, SCL0, SA4, None, None, None, None), # GPIO PIN 1
    (DIGITAL_IN, DIGITAL_OUT, SDA1, SA3, None, None, None, None), # GPIO PIN 2
    (DIGITAL_IN, DIGITAL_OUT, SCL1, SA2, None, None, None, None), # GPIO PIN 3
    (DIGITAL_IN, DIGITAL_OUT, GPCLK0, SA1, None, None, None, ARM_TDI), # GPIO PIN 4
    (DIGITAL_IN, DIGITAL_OUT, GPCLK1, SA0, None, None, None, ARM_TDO), # GPIO PIN 5
    (DIGITAL_IN, DIGITAL_OUT, GPCLK2, SOE_SE, None, None, None, ARM_RTCK), # GPIO PIN 6
    (DIGITAL_IN, DIGITAL_OUT, SPI0_CE1, SWE_SRW, None, None, None, None), # GPIO PIN 7
    (DIGITAL_IN, DIGITAL_OUT, SPI0_CE0, SD0, None, None, None, None), # GPIO PIN 8
    (DIGITAL_IN, DIGITAL_OUT, SPI0_MSIO, SD1, None, None, None, None), # GPIO PIN 9
    (DIGITAL_IN, DIGITAL_OUT, SPI0_MOSI, SD2, None, None, None, None), # GPIO PIN 10
    (DIGITAL_IN, DIGITAL_OUT, SPI0_SCLK, SD3, None, None, None, None), # GPIO PIN 11
    (DIGITAL_IN, DIGITAL_OUT, PWM0, SD4, None, None, None, ARM_TMS), # GPIO PIN 12
    (DIGITAL_IN, DIGITAL_OUT, PWM1, SD5, None, None, None, ARM_TCK), # GPIO PIN 13
    (DIGITAL_IN, DIGITAL_OUT, TXD0, SD6, None, None, None, TXD1), # GPIO PIN 14
    (DIGITAL_IN, DIGITAL_OUT, RXD0, SD7, None, None, None, RXD1), # GPIO PIN 15
    (DIGITAL_IN, DIGITAL_OUT, None, SD8, None, CTS0, None, CTS1), # GPIO PIN 16
    (DIGITAL_IN, DIGITAL_OUT, None, SD9, None, RTS0, None, RTS1), # GPIO PIN 17
    (DIGITAL_IN, DIGITAL_OUT, PCM_CLK, SD10, None, BSCSL_SDA_MOSI, SPI1_CE0, PWM0), # GPIO PIN 18
    (DIGITAL_IN, DIGITAL_OUT, PCM_FS, SD11, None, BSCSL_SCL_SCLK, SPI1_MSIO, PWM1), # GPIO PIN 19
    (DIGITAL_IN, DIGITAL_OUT, PCM_DIN, SD12, None, BSCSL_MSIO, SPI1_MOSI, GPCLK0), # GPIO PIN 20
    (DIGITAL_IN, DIGITAL_OUT, PCM_DOUT, SD13, None, BSCSL_CE, SPI1_SCLK, GPCLK1), # GPIO PIN 21
    (DIGITAL_IN, DIGITAL_OUT, None, SD14, None, SD1_CLK, ARM_TRST, None), # GPIO PIN 22
    (DIGITAL_IN, DIGITAL_OUT, None, SD15, None, SD1_CMD, ARM_RTCK, None), # GPIO PIN 23
    (DIGITAL_IN, DIGITAL_OUT, None, SD16, None, SD1_DAT0, ARM_TDO, None), # GPIO PIN 24
    (DIGITAL_IN, DIGITAL_OUT, None, SD17, None, SD1_DAT1, ARM_TCK, None), # GPIO PIN 25
    (DIGITAL_IN, DIGITAL_OUT, None, None, None, SD1_DAT2, ARM_TDI, None), # GPIO PIN 26
    (DIGITAL_IN, DIGITAL_OUT, None, None, None, SD1_DAT3, ARM_TMS, None), # GPIO PIN 27
    (DIGITAL_IN, DIGITAL_OUT, SDA0, SA5, PCM_CLK, None, None, None), # GPIO PIN 28
    (DIGITAL_IN, DIGITAL_OUT, SCL0, SA4, PCM_FS, None, None, None), # GPIO PIN 29
    (DIGITAL_IN, DIGITAL_OUT, None, SA3, PCM_DIN, CTS0, None, CTS1), # GPIO PIN 30
    (DIGITAL_IN, DIGITAL_OUT, None, SA2, PCM_DOUT, RTS0, None, RTS1), # GPIO PIN 31
    (DIGITAL_IN, DIGITAL_OUT, GPCLK0, SA1, None, TXD0, None, TXD1), # GPIO PIN 32
    (DIGITAL_IN, DIGITAL_OUT, None, SA0, None, RXD0, None, RXD1), # GPIO PIN 33
    (DIGITAL_IN, DIGITAL_OUT, GPCLK0, SOE_SE, None, None, None, None), # GPIO PIN 34
    (DIGITAL_IN, DIGITAL_OUT, SPI0_CE1, SWE_SRW, None, None, None, None), # GPIO PIN 35
    (DIGITAL_IN, DIGITAL_OUT, SPI0_CE0, SD0, TXD0, None, None, None), # GPIO PIN 36
    (DIGITAL_IN, DIGITAL_OUT, SPI0_MSIO, SD1, RXD0, None, None, None), # GPIO PIN 37
    (DIGITAL_IN, DIGITAL_OUT, SPI0_MOSI, SD2, RTS0, None, None, None), # GPIO PIN 38
    (DIGITAL_IN, DIGITAL_OUT, SPI0_SCLK, SD3, CTS0, None, None, None), # GPIO PIN 39
    (DIGITAL_IN, DIGITAL_OUT, PWM0, SD4, None, None, SPI2_MSIO, TXD1), # GPIO PIN 40
    (DIGITAL_IN, DIGITAL_OUT, PWM1, SD5, None, None, SPI2_MOSI, RXD1), # GPIO PIN 41
    (DIGITAL_IN, DIGITAL_OUT, GPCLK1, SD6, None, None, SPI2_SCLK, RTS1), # GPIO PIN 42
    (DIGITAL_IN, DIGITAL_OUT, GPCLK2, SD7, None, None, SPI2_CE0, CTS1), # GPIO PIN 43
    (DIGITAL_IN, DIGITAL_OUT, GPCLK1, SDA0, SDA1, None, SPI2_CE1, None), # GPIO PIN 44
    (DIGITAL_IN, DIGITAL_OUT, PWM1, SCL0, SCL1, None, SPI2_CE2, None), # GPIO PIN 45
    (DIGITAL_IN, DIGITAL_OUT, None, None, None, None, None, None), # GPIO PIN 46
    (DIGITAL_IN, DIGITAL_OUT, None, None, None, None, None, None), # GPIO PIN 47
    (DIGITAL_IN, DIGITAL_OUT, None, None, None, None, None, None), # GPIO PIN 48
    (DIGITAL_IN, DIGITAL_OUT, None, None, None, None, None, None), # GPIO PIN 49
    (DIGITAL_IN, DIGITAL_OUT, None, None, None, None, None, None), # GPIO PIN 50
    (DIGITAL_IN, DIGITAL_OUT, None, None, None, None, None, None), # GPIO PIN 51
    (DIGITAL_IN, DIGITAL_OUT, None, None, None, None, None, None), # GPIO PIN 52
    (DIGITAL_IN, DIGITAL_OUT, None, None, None, None, None, None), # GPIO PIN 53
]

# bit configurations for the different functions
_func_bits = [
    0x0, # input
    0x1, # output
    0x4, # alt func 0
    0x5, # alt func 1
    0x6, # alt func 2
    0x7, # alt func 3
    0x3, # alt func 4
    0x2, # alt func 5
]

# tells whether a GPIO pin is accessible
# on the RPi connector or not
_gpio_accessible = [
    True, # GPIO PIN 0
    True, # GPIO PIN 1
    False, # GPIO PIN 2
    False, # GPIO PIN 3
    True, # GPIO PIN 4
    False, # GPIO PIN 5
    False, # GPIO PIN 6
    True, # GPIO PIN 7
    True, # GPIO PIN 8
    True, # GPIO PIN 9
    True, # GPIO PIN 10
    True, # GPIO PIN 11
    False, # GPIO PIN 12
    False, # GPIO PIN 13
    True, # GPIO PIN 14
    True, # GPIO PIN 15
    False, # GPIO PIN 16
    True, # GPIO PIN 17
    True, # GPIO PIN 18
    False, # GPIO PIN 19
    False, # GPIO PIN 20
    True, # GPIO PIN 21
    True, # GPIO PIN 22
    True, # GPIO PIN 23
    True, # GPIO PIN 24
    True, # GPIO PIN 25
    False, # GPIO PIN 26
    False, # GPIO PIN 27
    False, # GPIO PIN 28
    False, # GPIO PIN 29
    False, # GPIO PIN 30
    False, # GPIO PIN 31
    False, # GPIO PIN 32
    False, # GPIO PIN 33
    False, # GPIO PIN 34
    False, # GPIO PIN 35
    False, # GPIO PIN 36
    False, # GPIO PIN 37
    False, # GPIO PIN 38
    False, # GPIO PIN 39
    False, # GPIO PIN 40
    False, # GPIO PIN 41
    False, # GPIO PIN 42
    False, # GPIO PIN 43
    False, # GPIO PIN 44
    False, # GPIO PIN 45
    False, # GPIO PIN 46
    False, # GPIO PIN 47
    False, # GPIO PIN 48
    False, # GPIO PIN 49
    False, # GPIO PIN 50
    False, # GPIO PIN 51
    False, # GPIO PIN 52
    False, # GPIO PIN 53
]


def _find_func_index(gpio, func):
    '''Returns the index in the 8 functions array
    for the given function. If the function is not available,
    -1 is returned.
    @param gpio: the number of the GPIO pin
    @param func: the desired function
    '''
    
    functions = _functions[gpio]
    for i in xrange(len(functions)):
        if functions[i] == func:
            return i

    return -1


def func_available(gpio, func):
    '''Tells whether a given function is available
    on the GPIO or not.
    @param gpio: the number of the GPIO pin
    @param func: the desired function
    '''
    
    if func < 0 or func > MAX_FUNC:
        raise Exception('Invalid GPIO number')

    if gpio < 0 or gpio > MAX_GPIO:
        raise Exception('Invalid GPIO number')

    return _find_func_index(gpio, func) >= 0


def gpio_accessible(gpio):
    '''Tells whether a given GPIO pin is available
    on the RPi connector or not.
    @param gpio: the number of the GPIO pin
    '''
    
    if gpio < 0 or gpio > MAX_GPIO:
        raise Exception('Invalid GPIO number')

    return _gpio_accessible[gpio]


def set_gpio_func(gpio, func):
    '''Sets the alternative function of the given
    GPIO pin.
    @param gpio: the number of the GPIO pin
    @param func: the desired function
    '''
    
    if func < 0 or func > MAX_FUNC:
        raise Exception('Invalid GPIO number')

    if gpio < 0 or gpio > MAX_GPIO:
        raise Exception('Invalid GPIO number')

    gpfsel_no = gpio // 10
    gpf_bit_start = (gpio % 10) * 3

    func_index = _find_func_index(gpio, func)
    if func_index == -1:
        raise Exception('Function not available on GPIO pin')

    func_bits = _func_bits[func_index]

    clr_value = ~(0x7 << gpf_bit_start)
    set_value = (func_bits << gpf_bit_start)

    if gpfsel_no == 0:
        regs.GPFSEL0 &= clr_value
        regs.GPFSEL0 |= set_value

    elif gpfsel_no == 1:
        regs.GPFSEL1 &= clr_value
        regs.GPFSEL1 |= set_value

    elif gpfsel_no == 2:
        regs.GPFSEL2 &= clr_value
        regs.GPFSEL2 |= set_value

    elif gpfsel_no == 3:
        regs.GPFSEL3 &= clr_value
        regs.GPFSEL3 |= set_value

    elif gpfsel_no == 4:
        regs.GPFSEL4 &= clr_value
        regs.GPFSEL4 |= set_value

    elif gpfsel_no == 5:
        regs.GPFSEL5 &= clr_value
        regs.GPFSEL5 |= set_value
