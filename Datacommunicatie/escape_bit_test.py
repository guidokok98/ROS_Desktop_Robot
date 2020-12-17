# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 17:58:35 2020

@author: guido
"""
import serial
import struct

#Define different bytes
start_byte = b'\x55'
stop_byte = b'\x5A'  
offLimit_Byte = b'\x5B' #off limit bc it turns in stop byte if 1 is subtracted
escape_byte = b'\x50'
Ack = b'\xF0'
NAck = b'\x0F'
cmd_angles = b'\x20'
defined_bytes = [start_byte, stop_byte, escape_byte, Ack, NAck, cmd_angles]

#adding
chkPayload = bytearray(b'P \x1f\x85\x9dA\xaeG\xabAq=\xb4B\x16')
print([ "0x%02x" % b for b in chkPayload])
chkPayloadTemp = bytearray()
#cycles through the payload
for i in range(0, len(chkPayload),1):
    chkByte = bytes([chkPayload[i]]) 
    #checks if the chkByte is one of the defined bytes
    for j in defined_bytes:
        #if chkbyte is the same as a define byte place an escape_byte 
        if chkByte == j: 
            print("hebbes")
            chkPayloadTemp.extend(escape_byte)
            print([ "0x%02x" % b for b in chkPayloadTemp])
            chkByte = bytes([(int.from_bytes(chkByte, "little")-1)])
    #adds the chkByte after the byte is checked if it is the same as a defined byte
    chkPayloadTemp.extend(chkByte)
    print([ "0x%02x" % b for b in chkPayloadTemp])
#returns the new payload
print([ "0x%02x" % b for b in chkPayloadTemp])

#win 10: ['0x50', '0x4f', '0x50', '0x1f', '0x1f', '0x85', '0x9d', '0x41', '0xae', '0x47', '0xab', '0x41', '0x71', '0x3d', '0xb4', '0x42', '0x16']
#subtracting escape bits


 # print([ "0x%02x" % b for b in chkPayload])
print("subtracting escape bit")
found = 0
chkPayload = chkPayloadTemp
chkPayloadTemp = bytearray()
#cycles through the payload
for i in range(0, len(chkPayload),1):
    chkByte = bytes([chkPayload[i]]) 
    #checks if the chkByte is one of the defined bytes
    if found == True:
        chkByte = bytes([(int.from_bytes(chkByte, "little")+1)])
        found = False
        
    elif chkByte == escape_byte:
        print("hebbes2")
        found = True
        
    #adds the chkByte after the byte is checked if it is the same as a defined byte
    if found == False:
        chkPayloadTemp.extend(chkByte)
    print([ "0x%02x" % b for b in chkPayloadTemp])
#returns the new payload
print([ "0x%02x" % b for b in chkPayloadTemp])

#win10: ['0x50', '0x20', '0x1f', '0x85', '0x9d', '0x41', '0xae', '0x47', '0xab', '0x41', '0x71', '0x3d', '0xb4', '0x42', '0x16'] (not correct?)