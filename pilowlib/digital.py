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

'''Sets or reads the digital value of a given GPIO pin.
'''

import funcs
import regs


def set_value(gpio, value):
    '''Sets the digital value of a given GPIO pin.
    @param gpio: the number of the GPIO pin
    @param value: a boolean indicating the new pin value
    '''
    
    if gpio < 0 or gpio > funcs.MAX_GPIO:
        raise Exception('Invalid GPIO number')

    reg_no = gpio // 32
    bit_no = gpio % 32

    if value:
        if reg_no == 0:
            regs.GPSET0 = 1 << bit_no

        elif reg_no == 1:
            regs.GPSET1 = 1 << bit_no

    else:
        if reg_no == 0:
            regs.GPCLR0 = 1 << bit_no

        elif reg_no == 1:
            regs.GPCLR1 = 1 << bit_no


def get_value(gpio):
    '''Reads and returns the digital value of a given
    GPIO pin.
    @param gpio: the number of the GPIO pin
    '''
    
    if gpio < 0 or gpio > funcs.MAX_GPIO:
        raise Exception('Invalid GPIO number')

    reg_no = gpio // 32
    bit_no = gpio % 32

    if reg_no == 0:
        return bool(regs.GPLEV0 & (1 << bit_no))

    elif reg_no == 1:
        return bool(regs.GPLEV1 & (1 << bit_no))
