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

'''This module provides raw access to the registers of the
RPi peripherals, as documented in the BCM2835 datasheet.
'''

import mmap
import os
import struct
import sys

_PAGE_SIZE = 4096 # RPi kernel page size

_BCM2708_PERI_BASE = 0x20000000 # RPi peripherals start address
_ST_BASE =           0x00003000 # System Timer offset address
_TMR_BASE =          0x0000B000 # Timer regs offset address
_PADS_BASE =         0x00100000 # Pads regs offset address
_CLK_BASE =          0x00101000 # Clock regs offset address
_GPIO_BASE =         0x00200000 # GPIO regs offset address
_UART_BASE =         0x00201000 # UART regs offset address
_PCM_BASE =          0x00203000 # PCM regs offset address
_SPI0_BASE =         0x00204000 # SPI0 regs offset address
_BSC0_BASE =         0x00205000 # BSC0 regs offset address
_PWM_BASE =          0x0020C000 # PWM regs offset address
_BSC_SPI_BASE =      0x00214000 # BSC SPI regs offset address
_AUX_BASE =          0x00215000 # AUX regs offset address
_BSC1_BASE =         0x00804000 # BSC1 regs offset address
_BSC2_BASE =         0x00805000 # BSC2 regs offset address

_tmr_mem = [] # provides raw access to the Timer regs mapped memory
_clk_mem = [] # provides raw access to the Clock regs mapped memory
_gpio_mem = [] # provides raw access to the GPIO regs mapped memory
_pcm_mem = [] # provides raw access to the PCM regs mapped memory
_pwm_mem = [] # provides raw access to the PWM regs mapped memory
_spi0_mem = [] # provides raw access to the SPI0 regs mapped memory


def _map_periph_memory():
    '''Calls 'mmap' for each memory page
    and sets the corresponding global _*_mem objects
    to the mapped memory objects.'''
    
    # open /dev/mem
    dev_mem = os.open('/dev/mem', os.O_RDWR | os.O_SYNC)

    # mmap the Timer
    global _tmr_mem
    _tmr_mem = mmap.mmap(
            dev_mem,
            length=_PAGE_SIZE,
            flags=mmap.MAP_SHARED,
            prot=mmap.PROT_READ | mmap.PROT_WRITE,
            offset=_BCM2708_PERI_BASE + _TMR_BASE)

    # map the Clock
    global _clk_mem
    _clk_mem = mmap.mmap(
            dev_mem,
            length=_PAGE_SIZE,
            flags=mmap.MAP_SHARED,
            prot=mmap.PROT_READ | mmap.PROT_WRITE,
            offset=_BCM2708_PERI_BASE + _CLK_BASE)

    # mmap the GPIO
    global _gpio_mem
    _gpio_mem = mmap.mmap(
            dev_mem,
            length=_PAGE_SIZE,
            flags=mmap.MAP_SHARED,
            prot=mmap.PROT_READ | mmap.PROT_WRITE,
            offset=_BCM2708_PERI_BASE + _GPIO_BASE)

    # map the PCM
    global _pcm_mem
    _pcm_mem = mmap.mmap(
            dev_mem,
            length=_PAGE_SIZE,
            flags=mmap.MAP_SHARED,
            prot=mmap.PROT_READ | mmap.PROT_WRITE,
            offset=_BCM2708_PERI_BASE + _PCM_BASE)

    # map the PWM
    global _pwm_mem
    _pwm_mem = mmap.mmap(
            dev_mem,
            length=_PAGE_SIZE,
            flags=mmap.MAP_SHARED,
            prot=mmap.PROT_READ | mmap.PROT_WRITE,
            offset=_BCM2708_PERI_BASE + _PWM_BASE)

    # map the PWM
    global _spi0_mem
    _spi0_mem = mmap.mmap(
            dev_mem,
            length=_PAGE_SIZE,
            flags=mmap.MAP_SHARED,
            prot=mmap.PROT_READ | mmap.PROT_WRITE,
            offset=_BCM2708_PERI_BASE + _SPI0_BASE)


class _Register(object):
    '''Represents a single register.
    Defines a setter and a getter to allow
    reading and assigning values with a simple syntax:
        regs.REG1 = 0xDEADBEEF'''
    
    def __init__(self, periph, offs, len=4):
        '''Constructs a register variable assigned to
        the given peripheral, address offset and length.
        @param periph: the name of the peripheral (e.g. "pwm")
        @param offs: the offset in the peripheral's mapped memory
        @param len: the length of the register in bytes, normally 4
        '''
        
        self.periph = periph
        self.offs = offs
        self.len = len
    
    @property
    def mem(self):
        '''Allows raw access to the peripheral memory
        associated with this register.'''
        
        return {
            'tmr': _tmr_mem,
            'clk': _clk_mem,
            'gpio': _gpio_mem,
            'pcm': _pcm_mem,
            'pwm': _pwm_mem,
            'spi0': _spi0_mem,
        }[self.periph]
        
    def get(self):
        '''Returns the value of the register as an integer.'''
        
        s = self.mem[self.offs:self.offs + self.len]
        
        return struct.unpack('I', s)[0]

    def set(self, value):
        '''Sets the value of the register.
        @param value: the value (an integer) to set'''
        
        s = struct.pack('I', value)
        
        self.mem[self.offs:self.offs + self.len] = s


class _ModuleWrapper(object):
    '''A class that wraps the 'regs' module
    by redefining setters and getters for the registers.'''
    
    def __init__(self, module):
        self.module = module

    def __getattr__(self, name):
        value = getattr(self.module, name)
        if isinstance(value, _Register):
            return value.get()

        else:
            return value

    def __setattr__(self, name, value):
        if name == 'module':
            self.__dict__[name] = value

        else:
            old_value = getattr(self.module, name)
            if isinstance(old_value, _Register):
                old_value.set(value)

            else:
                setattr(self.module, name, value)


def _wrap_module():
    sys.modules[__name__] = _ModuleWrapper(sys.modules[__name__])


# Timer registers
TMRLD = _Register('tmr', 0x400)
TMRVAL = _Register('tmr', 0x404)
TMRCTL = _Register('tmr', 0x408)
TMRIRQCA = _Register('tmr', 0x40C)
TMRIRQR = _Register('tmr', 0x410)
TMRIRQM = _Register('tmr', 0x414)
TMRRLD = _Register('tmr', 0x418)
TMRDIV = _Register('tmr', 0x41C)
TMRFRC = _Register('tmr', 0x420)

# Clock registers
CLKGP0CTL = _Register('clk', 0x70)
CLKGP0DIV = _Register('clk', 0x74)
CLKGP1CTL = _Register('clk', 0x78)
CLKGP1DIV = _Register('clk', 0x7C)
CLKGP2CTL = _Register('clk', 0x80)
CLKGP2DIV = _Register('clk', 0x84)
CLKPWMCTL = _Register('clk', 0xA0)
CLKPWMDIV = _Register('clk', 0xA4)

# GPIO registers
GPFSEL0 = _Register('gpio', 0x00)
GPFSEL1 = _Register('gpio', 0x04)
GPFSEL2 = _Register('gpio', 0x08)
GPFSEL3 = _Register('gpio', 0x0C)
GPFSEL4 = _Register('gpio', 0x10)
GPFSEL5 = _Register('gpio', 0x14)
GPSET0 = _Register('gpio', 0x1C)
GPSET1 = _Register('gpio', 0x20)
GPCLR0 = _Register('gpio', 0x28)
GPCLR1 = _Register('gpio', 0x2C)
GPLEV0 = _Register('gpio', 0x34)
GPLEV1 = _Register('gpio', 0x38)
GPEDS0 = _Register('gpio', 0x40)
GPEDS1 = _Register('gpio', 0x44)
GPREN0 = _Register('gpio', 0x4C)
GPREN1 = _Register('gpio', 0x50)
GPFEN0 = _Register('gpio', 0x58)
GPFEN1 = _Register('gpio', 0x5C)
GPHEN0 = _Register('gpio', 0x64)
GPHEN1 = _Register('gpio', 0x68)
GPLEN0 = _Register('gpio', 0x70)
GPLEN1 = _Register('gpio', 0x74)
GPAREN0 = _Register('gpio', 0x7C)
GPAREN1 = _Register('gpio', 0x80)
GPAFEN0 = _Register('gpio', 0x88)
GPAFEN1 = _Register('gpio', 0x8C)
GPPUD = _Register('gpio', 0x94)
GPPUDCLK0 = _Register('gpio', 0x98)
GPPUDCLK1 = _Register('gpio', 0x9C)

# PCM registers
PCMCS = _Register('pcm', 0x00)
PCMFIFO = _Register('pcm', 0x04)
PCMMODE = _Register('pcm', 0x08)
PCMRXC = _Register('pcm', 0x0C)
PCMTXC = _Register('pcm', 0x10)
PCMDREQ = _Register('pcm', 0x14)
PCMINTEN = _Register('pcm', 0x18)
PCMINTSTC = _Register('pcm', 0x1C)
PCMGRAY = _Register('pcm', 0x20)

# PWM registers
PWMCTL = _Register('pwm', 0x00)
PWMSTA = _Register('pwm', 0x04)
PWMDMAC = _Register('pwm', 0x08)
PWMRNG0 = _Register('pwm', 0x10)
PWMDAT0 = _Register('pwm', 0x14)
PWMFIF = _Register('pwm', 0x18)
PWMRNG1 = _Register('pwm', 0x20)
PWMDAT1 = _Register('pwm', 0x24)

# SPI0 registers
SPI0CS = _Register('spi0', 0x00)
SPI0FIFO = _Register('spi0', 0x04)
SPI0CLK = _Register('spi0', 0x08)
SPI0DLEN = _Register('spi0', 0x0C)
SPI0LTOH = _Register('spi0', 0x10)
SPI0DC = _Register('spi0', 0x04)

# perform the memory mappings, as well as
# wrapping the module as soon as the module
# is imported for the first time
_map_periph_memory()
_wrap_module()
