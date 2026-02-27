import serial
import time

serial_port = 'COM7'
baud_rate = 115200

ser = serial.Serial(serial_port, baud_rate)

time.sleep(2)

ser.write(b"f=open('log.txt', 'r)\r\n")
line = ser.readline().decode('utf-8').strip()

with open('log.txt', 'w') as file:
    while line != "''":
        ser.write(b"f.readline()\r\n")
        line = ser.readline().decode('utf-8').strip()
        time.sleep(1)
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("'"):
            line = line[1: -3]
            file.write(line + '\n')

ser.write(b"f.close()\r\n")
ser.close()