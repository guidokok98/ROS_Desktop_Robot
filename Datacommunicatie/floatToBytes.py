# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 10:38:55 2020

@author: guido
"""

import struct

payload_temp = bytearray()
payload_temp.extend(struct.pack("f", 19.68))

print([ "0x%02x" % b for b in payload_temp])

#win 10 result = ['0xa4', '0x70', '0x9d', '0x41']