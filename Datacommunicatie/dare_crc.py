# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 15:34:41 2020

@author: guido
"""

def crc8(crc0,data):
    crc = crc0 ^ data #crc - data
    print(f'{bin(crc0)} ^ {bin(data)} = {bin(crc)} \t ({crc})')
    print(f'0x8c = {bin(0x8c)}')
    for i in range(8):
        print('\n')
        if (crc & 1): # checks if last bit is 1
            print('\t \t shift to right')
            print(f'i = {i} \t crc = {bin(crc>>1)}')
            print('\t \t XOR')
            print(f'\t \t 0x8c= {bin(0x8c)}')
            crc = (crc >> 1) ^ 0b10001100
            print('\t \t =')
            print(f'i = {i} \t crc = {bin(crc)} \t ({crc})')
        else:
            print(f'i = {i} \t crc = {bin(crc)}')
            print('\t \t shift to right')
            crc = (crc >> 1)
            print(f'i = {i} \t crc = {bin(crc)} \t ({crc})')
    return crc

x = crc8(0, 0b11001011)
print('\n')
print(f'x = {x}')
print('\n')
x = crc8(x, 0b01101011)
print('\n')
print(f'x = {x}')