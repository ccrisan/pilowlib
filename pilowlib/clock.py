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

'''Provides configuration and control functions for the RPi clocks.
There are 3 general purpose clocks (numbered from 0 to 2)
and a clock that drives the PWM peripherals, identified as 'pwm'.
'''

import regs

# clock sources
SRC_GND = 0
SRC_OSC = 1
SRC_TEST_DEBUG0 = 2
SRC_TEST_DEBUG1 = 3
SRC_PLLA = 4
SRC_PLLB = 5
SRC_PLLC = 6
SRC_HDMI_AUX = 7


def configure(clock_no, src, div):
    '''Sets a clock's source and divisor.
    @param clock_no: the identifier of the clock (0, 1, 2 or 'pwm')
    @param src: the clock source, one of the SRC_* constants
    '''

    if clock_no != 'pwm' and (clock_no < 0 or clock_no > 2):
        raise Exception('Invalid clock number')

    if src < 0 or src > 7:
        raise Exception('Invalid clock source')

    if div < 0 or div > 0xFFF:
        raise Exception('Invalid clock divider')

    ctl = 0x5A000000 + src
    div = 0x5A000000 + (div << 12)

    if clock_no == 'pwm':
        regs.CLKPWMCTL = ctl
        regs.CLKPWMDIV = div

    elif clock_no == 0:
        regs.CLKGP0CTL = ctl
        regs.CLKGP0DIV = div

    elif clock_no == 1:
        regs.CLKGP1CTL = ctl
        regs.CLKGP1DIV = div

    elif clock_no == 2:
        regs.CLKGP2CTL = ctl
        regs.CLKGP2DIV = div


def start(clock_no):
    '''Starts a clock.
    @param clock_no: the identifier of the clock (0, 1, 2 or 'pwm')
    '''

    if clock_no != 'pwm' and (clock_no < 0 or clock_no > 2):
        raise Exception('Invalid clock number')

    ctl = 0x5A000010

    if clock_no == 'pwm':
        regs.CLKPWMCTL |= ctl

    elif clock_no == 0:
        regs.CLKGP0CTL |= ctl

    elif clock_no == 1:
        regs.CLKGP1CTL |= ctl

    elif clock_no == 2:
        regs.CLKGP2CTL |= ctl


def stop(clock_no):
    '''Stops a clock.
    @param clock_no: the identifier of the clock (0, 1, 2 or 'pwm')
    '''

    if clock_no != 'pwm' and (clock_no < 0 or clock_no > 2):
        raise Exception('Invalid clock number')

    ctl = 0x5A000000 + ~0x000010

    if clock_no == 'pwm':
        regs.CLKPWMCTL &= ctl

    elif clock_no == 0:
        regs.CLKGP0CTL &= ctl

    elif clock_no == 1:
        regs.CLKGP1CTL &= ctl

    elif clock_no == 2:
        regs.CLKGP2CTL &= ctl


def is_busy(clock_no):
    '''Tells whether a clock is busy or not.
    @param clock_no: the identifier of the clock (0, 1, 2 or 'pwm')
    '''

    if clock_no != 'pwm' and (clock_no < 0 or clock_no > 2):
        raise Exception('Invalid clock number')

    if clock_no == 'pwm':
        return regs.CLKPWMCTL & 0x80

    elif clock_no == 0:
        return regs.CLKGP0CTL & 0x80

    elif clock_no == 1:
        return regs.CLKGP1CTL & 0x80

    elif clock_no == 2:
        return regs.CLKGP2CTL & 0x80
