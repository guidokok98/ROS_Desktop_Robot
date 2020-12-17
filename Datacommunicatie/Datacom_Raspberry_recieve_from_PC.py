# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 11:40:53 2020

@author: Guido Kok
To do:
    - filter the escape_byte
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
cmd_pathDone = b'\x30'
defined_bytes = [start_byte, stop_byte, escape_byte, Ack, NAck, cmd_angles,cmd_pathDone]



#start serial communication, and checks if communication works
def startSerial(port, baudrate, timeout):
    global ser
    #starts serial communication with given parameters
    ser = serial.Serial(port , baudrate, timeout = timeout)
    serInput = ser.read(1)
    while serInput != Ack:
        ser.write(NAck)
        serInput = ser.read(1)
        
    if serInput == Ack:
        ser.write(Ack)
        return True
    else:
        ser.write(NAck)
        return False

def serialRead(crcPol):
    crc = False
    while crc == False:
        byte1 = ser.read(1)
        if byte1 == start_byte:
            payload = ser.read_until(stop_byte)
            #get rid of the stop byte
            payload = payload[:(len(payload)-1)]
            #checks the crc
            crc,payload = calcCrc(payload, crcPol, "receive")
            #get rid of the escape byte
            payload = checkPayload(payload)
            #check if crc are equel to each other
            if crc == True:
                ser.write(Ack)
            else:
                ser.write(NAck)
    return bytes([payload[0]]),payload[1:]

#calculates crc of the payload (working with little)
def calcCrc(crcPayload, crcPol, modus):
    if modus == "transmit":
        crcPayload.extend(b'\x00')

    pol_size = 0
    while (crcPol >> pol_size) > 0:
        pol_size +=1
        
    crcVal = 0
    for i in range(0, len(crcPayload), 1): #i is the counter for the crcPayload bytes
            crcVal = crc8(crcVal, crcPayload[i], crcPol, pol_size)
    
    #if in transmit modus, voeg crcVal toe aan de payload en return payload
    if modus == "transmit":
        crcPayload[len(crcPayload)-1] = crcVal
        return crcPayload
    #if in receive modus, check de crcVal
    if modus == "receive":
        #if crcVal == 0 alle bytes zijn goed ontvangen, ruturn een True en de orginele payload
        if crcVal == 0:
            crcPayload = crcPayload[0:(len(crcPayload)-1)]
            return True, crcPayload
        #if crcVal != 0, return een False en de payload.
        else:
            crcPayload = crcPayload[0:(len(crcPayload)-1)]
            return False, crcPayload

#clculates crc over een byte, returnt de crc_val
def crc8(crcVal, crc8Payload, crcPol, pol_size):
        for j in range(0, 8, 1): #j is the counter for the bit, crcPayload should be at leas a byte
                #add kijkt of er een1 of 0 toegevoegd moet worden aan de crcVal
                add = 1<< (7-j)
                add = crc8Payload & add
                add = add >> (7-j)
                #verleng de crcVal met 1 bit
                crcVal = crcVal << 1
                #voeg de add achteraan toen
                crcVal = crcVal | add 
                #checks if an xor can be done
                if (crcVal >> (pol_size-1) & 1): 
                    crcVal = crcVal ^ crcPol   
        return(crcVal)
    
#checks if escape bit is needed in payload, and places them
def checkPayload(chkPayload):
    found = 0
    chkPayloadTemp = bytearray()
    #cycles through the payload
    for i in range(0, len(chkPayload),1):
        chkByte = bytes([chkPayload[i]]) 
        #checks if the chkByte is one of the defined bytes
        if found == True:
            chkByte = bytes([(int.from_bytes(chkByte, "little")+1)])
            found = False
            
        elif chkByte == escape_byte:
            found = True
            
        #adds the chkByte after the byte is checked if it is the same as a defined byte
        if found == False:
            chkPayloadTemp.extend(chkByte)
    #returns the new payload
    return chkPayloadTemp

def bytesToFloats(inputBytes):
    # print([ "0x%02x" % b for b in inputBytes])
    output = []
    try:
        if len(inputBytes)%4 == 0:
            for i in range (0,(len(inputBytes)//4),1):
                val =struct.unpack("f", inputBytes[(i*4):(i*4)+4])[0]
                output.append(round(val,2))
    except:
        print("input not dividable by 4")
    return output


crcPol = 0b110011011
status = startSerial('/dev/ttyGS0',115200, 0.1)
completePath = []
while status == True:
    cmd, receivedBytes = serialRead(crcPol)
    if cmd == cmd_angles:    
        Angles = bytesToFloats(receivedBytes)
        completePath.append(Angles)
        print(f"BytesMeaning = {Angles}")
    
    if cmd == cmd_pathDone:
        print("path is done")
        break

# ser.close()
# print(completePath)
# print([ "0x%02x" % b for b in receivedBytes])
    

