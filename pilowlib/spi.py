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

'''Provides easy configuration and control for the SPI0
peripheral of the RPi.
'''

import regs
import utils


def configure(clock_rest_polarity=0, clock_phase=1, clock_divider=0, chip_select0=None, chip_select1=None):
    '''Configures the SPI peripheral.
    For further information on the way SPI works on the RPi,
    please refer to the BCM 2835 peripheral datasheet.
    @param clock_rest_polarity: sets the polarity of the clock signal
    when not transmitting data to either 0 or 1
    @param clock_phase: if set to 0, the clock transition will take place
    in the middle of the data bit; if set to 1, the clock transition happens
    at the beginning of the data bit
    @param clock_divider: a value between 0 and 65535 what divides
    the system clock in order to obtain the SPI clock signal
    @param chip_select0: if set to 1, chip select 0 will be held to 1
    when transmitting data; if set to 0, chip select 0 will be held to 0
    when transmitting data; if None is passed, chip select 0 will not be asserted
    at all during transmission 
    @param chip_select1: if set to 1, chip select 1 will be held to 1
    when transmitting data; if set to 0, chip select 1 will be held to 0
    when transmitting data; if None is passed, chip select 1 will not be asserted
    at all during transmission 
    '''
    value = 0
    
    if clock_rest_polarity:
        value |= 0x08
    
    if clock_phase:
        value |= 0x04
    
    if chip_select0 is not None:
        if chip_select1 is not None:
            value |= 0x02 # use both CS0 and CS1
 
    else:
        if chip_select1 is not None:
            value |= 0x01 # use only CS1
        
        else:
            value |= 0x03 # don't use any CS
    
    if chip_select0 == 1:
        value |= 0x200000

    if chip_select1 == 1:
        value |= 0x400000
    
    regs.SPI0CS = value
    
    # set the clock divider
    regs.SPI0CLK = clock_divider


def transfer_value(value):
    '''Reads and writes one byte from and to the SPI.
    @var value: the byte to write 
    @return: the byte that was read
    '''
    
    # clear the TX and RX fifos
    regs.SPI0CS |= 0x30
    
    # set the TA flag
    regs.SPI0CS |= 0x80
    
    # wait for TXD flag
    while regs.SPI0CS & 0x40000 == 0:
        utils.nanosleep(0, 5)
    
    # write the value to the TX fifo
    regs.SPI0FIFO = value & 0xFF
    
    # wait for DONE flag to be set
    while regs.SPI0CS & 0x10000 == 0:
        utils.nanosleep(0, 5)
    
    # read the received value
    value = regs.SPI0FIFO
    
    # clear the TA flag
    regs.SPI0CS &= 0xFFFFFF7F
    
    return value


def transfer_values(values):
    '''Reads and writes more bytes from and to the SPI.
    @var values: the list of bytes to write 
    @return: the bytes that were read
    '''
    
    # clear the TX and RX fifos
    regs.SPI0CS |= 0x30
    
    # set the TA flag
    regs.SPI0CS |= 0x80
    
    read_values = []
    
    for value in values:
        # wait for TXD flag to be set
        while regs.SPI0CS & 0x40000 == 0:
            utils.nanosleep(0, 5)
        
        # write the value to the TX fifo
        regs.SPI0FIFO = value & 0xFF
        
        # wait for RXD flag to be set
        while regs.SPI0CS & 0x20000 == 0:
            utils.nanosleep(0, 5)
        
        # read the received value
        read_values.append(regs.SPI0FIFO)
    
    # wait for DONE flag to be set
    while regs.SPI0CS & 0x10000 == 0:
        utils.nanosleep(0, 5)
    
    # clear the TA flag
    regs.SPI0CS &= 0xFFFFFF7F
    
    return read_values
