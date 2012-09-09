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
# the first PWM peripheral (PWM0) in a Raspberry PI using PiLowLib,
# setting the PWM output to GPIO number 18.

from pilowlib import funcs, pwm, clock


# sets the GPIO pin 18 to PWM0
funcs.set_gpio_func(18, funcs.PWM0)

# configures PWM0 with the default settings (plain PWM)
pwm.configure(0)

# set the PWM clock source to oscillator (said to be 19.2 MHz),
# and the divider to 32, resulting a 19.2MHz/32 = 600KHz
pwm.configure_clock(clock.SRC_OSC, 32)

# set the range to 1024 and the data to 512 for PWM0,
# resulting in a duty cycle of 50%
pwm.set_range(0, 1024)
pwm.set_data(0, 512)

# start the PWM0 peripheral
pwm.start(0)
