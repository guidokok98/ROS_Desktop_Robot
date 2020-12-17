# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 10:04:44 2020

@author: guido
"""
payload = bytearray(b'P\x1f\x1f\x85\x9dAPY\xc9Z')
# payload = bytearray(b'\x1f\x85\x9dA')
crc_pol = 0b110011011


def calcCrc(crcPayload, crc_pol, modus):
    if modus == "transmit":
        crcPayload.extend(b'\x00')

    pol_size = 0
    while (crc_pol >> pol_size) > 0:
        pol_size +=1
        
    crcVal = 0
    for i in range(0, len(crcPayload), 1): #i is the counter for the crcPayload bytes
            crcVal = crc8(crcVal, crcPayload[i], crc_pol, pol_size)
    
        # for j in range(0, 8, 1): #j is the counter for the bit, crcPayload should be at leas a byte
        #         #add kijkt of er een1 of 0 toegevoegd moet worden aan de crcVal
        #         add = 1<< (7-j)
        #         add = crcPayload[i] & add
        #         add = add >> (7-j)
        #         #verleng de crcVal met 1 bit
        #         crcVal = crcVal << 1
        #         #voeg de add achteraan toen
        #         crcVal = crcVal | add 
                
        #         if (crcVal >> (pol_size-1) & 1): #checks if an xor can be done
        #             crcVal = crcVal ^ crc_pol
        
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
        
def crc8(crcVal, crc8Payload, crc_pol, pol_size):
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
                    crcVal = crcVal ^ crc_pol   
        return(crcVal)
    
x = calcCrc(payload, crc_pol, "transmit")
print(f'transmit: {x}')
print(f'receive: {calcCrc(x, crc_pol, "receive")}')