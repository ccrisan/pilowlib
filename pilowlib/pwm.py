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

'''Provides easy configuration and control for the two
PWM peripherals of the RPi.
There are two PWM peripherals numbered 0 and 1.
'''

import clock
import regs


def configure(pwm_no, serial_mode=False, ms_mode=False, use_fifo=False, rep_fifo=False, high_off=False, rev_polarity=False):
    '''Configures a PWM peripheral (without starting it).
    For further information on the way PWM works on the RPi,
    please refer to the BCM 2835 peripheral datasheet.
    @param pwm_no: the identifier of the PWM peripheral (0 or 1)
    @param serial_mode: set to True to use the 'serializer' mode
    instead of the 'PWM' mode
    @param ms_mode: set to True to use 'M/S' instead of the PWM algorithm
    @param use_fife: set to True to use the FIFO instead of the PWM data register
    @param rep_fifo: set to True to repeat the last data in FIFO when FIFO is empty
    @param high_off: set to True to set the logic level to 'high' when
    no PWM data is transmitted
    @param rev_polarity: set to True to reverse the polarities of the PWM signal
    '''
    
    value = 0

    if serial_mode:
        value |= 0x02

    if ms_mode:
        value |= 0x80

    if use_fifo:
        value |= 0x20

    if rep_fifo:
        value |= 0x04

    if high_off:
        value |= 0x08

    if rev_polarity:
        value |= 0x10

    if pwm_no == 0:
        regs.PWMCTL &= ~0xFF;
        regs.PWMCTL |= value

    elif pwm_no == 1:
        value <<= 8

        regs.PWMCTL &= ~0xFF00;
        regs.PWMCTL |= value

    else:
        raise Exception('Invalid PWM number')


def configure_clock(src, div):
    '''Configures the clock used by the PWM peripherals.
    Warning: there is only one clock that drives both of the
    PWM peripherals, therefore changes to the clock will
    immediately affect both of them.
    @param src: the source of the clock
    (one of the clock.SRC_* constants)
    @param div: the divider (0..4095) 
    '''
    # the clock is configured separately
    clock.configure('pwm', src, div)


def set_data(pwm_no, data):
    '''Sets the data register for the given PWM peripheral.
    @param pwm_no: the identifier of the PWM (0 or 1)
    @param data: the value to set (an integer)
    '''
    if pwm_no == 0:
        regs.PWMDAT0 = data

    elif pwm_no == 1:
        regs.PWMDAT1 = data

    else:
        raise Exception('Invalid PWM number')


def set_range(pwm_no, range):
    '''Sets the data range used by a PWM peripheral.
    @param pwm_no: the identifier of the PWM (0 or 1)
    @param range: the value of the range to use (an integer)
    '''
    
    if pwm_no == 0:
        regs.PWMRNG0 = range

    elif pwm_no == 1:
        regs.PWMRNG1 = range

    else:
        raise Exception('Invalid PWM number')


def start(pwm_no):
    '''Starts a PWM peripheral.
    Also starts the clock that drives the PWM.
    @param pwm_no: the identifier of the PWM (0 or 1)
    '''
    
    if pwm_no == 0:
        regs.PWMCTL |= 0x01

    elif pwm_no == 1:
        regs.PWMCTL |= 0x100

    else:
        raise Exception('Invalid PWM number')

    # make sure the clock is started as well    
    clock.start('pwm')


def stop(pwm_no):
    '''Stops a PWM peripheral.
    Does not stop the clock that drives the PWM.
    @param pwm_no: the identifier of the PWM (0 or 1)
    '''
    
    if pwm_no == 0:
        regs.PWMCTL &= ~0x01

    elif pwm_no == 1:
        regs.PWMCTL &= ~0x100

    else:
        raise Exception('Invalid PWM number')


def add_fifo(value):
    '''Adds a value to the PWM FIFO.
    @param value: the value to add (am integer)
    '''
    
    regs.PWMFIF = value


def clear_fifo():
    '''Clears the PWM FIFO.
    '''
    
    regs.PWMCTL &= 0x40


def fifo_full():
    '''Tells whether the PWM FIFO is full or not.
    '''
    
    return regs.PWMSTA & 0x01


def fifo_empty():
    '''Tells whether the PWM FIFO is empty or not.
    '''
    
    return regs.PWMSTA & 0x02
