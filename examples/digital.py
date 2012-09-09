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

# This example shows how to configure and read/write two GPIO pins (18 and 23),
# one as a digital output and the other as a digital input.

from pilowlib import funcs, digital


# sets the GPIO pin 18 to digital out
funcs.set_gpio_func(18, funcs.DIGITAL_OUT)

# sets the GPIO pin 23 to digital in
funcs.set_gpio_func(23, funcs.DIGITAL_IN)

# sets the GPIO pin 18 to 'high' 
digital.set_value(18, True)

# reads the level of the GPIO pin 23 
value = digital.get_value(23)
if value:
    print('GPIO 23 is high')
    
else:
    print('GPIO 23 is low')
