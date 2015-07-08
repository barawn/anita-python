import ocpci
import struct
import sys
import time
from bf import * 


#
# This is the spi module
# surf.py and tisc.py need to import this module
#

class SPI:
    map = { 'SPCR'       : 0x000000,
            'SPSR'       : 0x000004,
            'SPDR'       : 0x000008,
            'SPER'       : 0x00000C }
    
    cmd = { 'RES'        : 0xAB ,
            'RDID'       : 0x9F ,
            'WREN'       : 0x06 ,
            'WRDI'       : 0x04 ,
            'RDSR'       : 0x05 ,
            'WRSR'       : 0x01 ,
            'READ'       : 0x03 ,
            'FASTREAD'   : 0x0B ,
            'PP'         : 0x02 ,
            'SE'         : 0xD8 ,
            'BE'         : 0xC7 }
    
    bits = { 'SPIF'      : 0x80,
             'WCOL'      : 0x40,
             'WFFULL'    : 0x08,
             'WFEMPTY'   : 0x04,
             'RFFULL'    : 0x02,
             'RFEMPTY'   : 0x01 }
    
    def __init__(self, dev, base, device = 0):
        self.dev = dev
        self.base = base
        self.device = device 
        val = bf(self.dev.read(self.base + self.map['SPCR']))
        val[6] = 1;
        val[3] = 0;
        val[2] = 0;
        self.dev.write(self.base + self.map['SPCR'], int(val))

    def command(self, command, dummy_bytes, num_read_bytes, data_in = [] ):
        self.dev.spi_cs(self.device, 1)
        self.dev.write(self.base + self.map['SPDR'], command)
        for dat in data_in:
            self.dev.write(self.base + self.map['SPDR'], dat)
        for i in range(dummy_bytes):
            self.dev.write(self.base + self.map['SPDR'], 0x00)
        # Empty the read FIFO.
        while not (self.dev.read(self.base + self.map['SPSR']) & self.bits['RFEMPTY']):
            self.dev.read(self.base + self.map['SPDR'])
        rdata = []
        for i in range(num_read_bytes):
            self.dev.write(self.base + self.map['SPDR'], 0x00)
            rdata.append(self.dev.read(self.base + self.map['SPDR']))
        self.dev.spi_cs(self.device, 0)    
        return rdata
    
    def identify(self):
        res = self.command(self.cmd['RES'], 3, 1)
        print "Electronic Signature: 0x%x" % res[0]
        res = self.command(self.cmd['RDID'], 0, 3)
        print "Manufacturer ID: 0x%x" % res[0]
        print "self.device ID: 0x%x 0x%x" % (res[1], res[2])

    def read(self, address, length=1):
        data_in = []
        data_in.append((address >> 16) & 0xFF)
        data_in.append((address >> 8) & 0xFF)
        data_in.append(address & 0xFF)
        res = self.command(self.cmd['READ'], 0, length, data_in)
        return res        
		
    def program(self, address, data):
        print "Inside function program: command to program the SPI flash" 
	
	
    def write_enable(self, status):
        print "Inside function write_enable: command to make SPI flash write enabled" 

	
    def write_disable(self):
        print "Inside function write_disable: command to make SPI flash write disabled" 
	
	
	
	
	
	
	