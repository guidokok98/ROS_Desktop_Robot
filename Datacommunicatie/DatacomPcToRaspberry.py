# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 11:25:43 2020
@author: Guido Kok

to convert from byte to int: int.from_bytes(b'\x55', "little")
to convert int to      byte: bytes([85]) 

To do:
    - what if crc is equel to stop byte? add escape byte?
    -signal when path transfer is done (when start and stop are right after each other)
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
    #Sends Ack to the Raspberry
    ser.write(Ack)
    #reads the response from the raspberry, should be one byte
    serInput = ser.read(1)
    while serInput != Ack:
        ser.write(Ack)
        serInput = ser.read(1)
    #if an Ack is received, datacom is working
    if serInput == Ack:
        return ser,True
    #received something else or timeout, datatcom is not working!
    else:
        ser.close()
        return ser,False
    

#function to send data 
def serialSend(cmd_byte, data, crcPol):
    global payload
    #put the data in a bytearray
    payload = bytearray()
    payload.extend(cmd_byte)
    if cmd_byte == cmd_angles:
        payload = payload+ float2byte(data)
    

    #checks if payload contains already defined bytes (stop_byte, escape_byte, etc) 
    payload = checkPayload(payload)
    #calculates the crc of the payload and returns payload with crc
    payload = calcCrc(payload, crcPol, "transmit")
    #adds start byte at the beginning of the payload
    payload[0:0] = start_byte
    #adds stop byte at the end of the payload
    payload.extend(stop_byte)
    #writes the payload to the raspberry
    serInput = NAck
    while serInput != Ack:
        ser.write(payload)
        serInput = ser.read(1)
        if serInput == Ack:
            return True
        # if serInput == NAck:
            #return false
            

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
            return False, crcPayload

#calculates crc over een byte, returnt de crc_val
def crc8(crcVal, crc8Payload, crcPol, pol_size):
        for j in range(0, 8, 1): #j is the counter for the bit, crcPayload should be at leas a byte
                #add kijkt of er een 1 of 0 toegevoegd moet worden aan de crcVal
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
    chkPayloadTemp = bytearray()
    #cycles through the payload
    for i in range(0, len(chkPayload),1):
        chkByte = bytes([chkPayload[i]]) 
        #checks if the chkByte is one of the defined bytes
        for j in defined_bytes:
            #if chkbyte is the same as a define byte place an escape_byte 
            if chkByte == j: 
                chkPayloadTemp.extend(escape_byte)
                chkByte = bytes([(int.from_bytes(chkByte, "little")-1)])
        #adds the chkByte after the byte is checked if it is the same as a defined byte
        chkPayloadTemp.extend(chkByte)
    #returns the new payload
    return chkPayloadTemp
    
#turns the floats into a bytearray, returns this bytearray
def float2byte(data):
    payload_temp = bytearray()
    for x in data:
        #puts all the data in bytes in the payload
        payload_temp.extend(struct.pack("f", x))
    return payload_temp


crcPol = 0b110011011
#starts the serial communication
ser, status = startSerial('COM9', 115200, 0.1)
#if the serial is working send the angels
while status == True:
    #loop for sending the angles
    serialSend(cmd_angles, [12.9], crcPol)
    serialSend(cmd_angles, [18.123, 1238.33], crcPol)
    serialSend(cmd_pathDone, [], crcPol)
    print([ "0x%02x" % b for b in payload])
    break;
ser.close()

"""
use this library as following (# are still commends):
    
crcPol = 0b110011011
#starts the serial communication
status = startSerial('COM9', 115200, 0.1)
#if the serial is working send the angels
while status == True:
    #loop for sending the angles
    serialSend("angles", [19.69], crcPol)
    ser.close()
    break;
"""