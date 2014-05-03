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

'''Various utilities used both internally by the library
and by other programs that use this library.
'''

import ctypes


# we define a nanosleep() function by importing it
# directly from libc (using ctypes);
# this code is partly taken from the Zope project
_libc_variants = ['libc.so.6', 'libc.so.5', 'libc.so.0', 'libc.so']

for _variant in _libc_variants:
    try:
        _libc = ctypes.CDLL(_variant)
        break
    
    except OSError:
        continue


class __timespec(ctypes.Structure):
    _fields_ = [('secs', ctypes.c_long), ('nsecs', ctypes.c_long)]

_libc.nanosleep.argtypes = [ctypes.POINTER(__timespec), ctypes.POINTER(__timespec)]


def nanosleep(sec, nsec):
    '''Stops the execution of the calling thread by
    a specified number of seconds and nanoseconds.
    @param sec: the number of seconds to sleep
    @param nsec: the number of nanoseconds to sleep
    '''

    sleeptime = __timespec()
    sleeptime.secs = sec
    sleeptime.nsecs = nsec
    remaining = __timespec()
    _libc.nanosleep(sleeptime, remaining)
