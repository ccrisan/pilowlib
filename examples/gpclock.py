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

# This example shows how to configure and control
# the first general purpose clock (GPCLK0) in a Raspberry PI using PiLowLib,
# setting the clock output to GPIO number 4.

from pilowlib import funcs, clock


# sets the GPIO pin 4 to GPCLK0
funcs.set_gpio_func(4, funcs.GPCLK0)

# set the GPCLK0 source to oscillator (said to be 19.2 MHz),
# and the divider to 32, resulting a 19.2MHz/32 = 600KHz
clock.configure(0, clock.SRC_OSC, 32)

# start the GPCLK0 peripheral
clock.start(0)

