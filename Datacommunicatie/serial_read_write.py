import serial
import struct
#use COM3 on windows and /dev/ttyGS0 /dev/serial0 on linux 
ser = serial.Serial('COM9',115200) 
#send byte
ser.write(b'\x55') 
#read serial
# ser.read()

#to send output
# ser.write(ba) 
# print("send")
#to read input
#while 1:
#    print(ser.read())

# ser.close()

# print("start")

# while 1:
    
#     if ser.read() == start_byte:
#         print("jazeker")
#         payload = ser.read_until(stop_byte)
#         del payload[len(payload)-1]
#         print([ "0x%02x" % b for b in payload])
#         break
        
#     else:
#         print(":(")
