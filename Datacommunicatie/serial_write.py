import serial
ser = serial.Serial('COM9',115200)

#to send output
ser.write(b'hello') 


ser.close()

