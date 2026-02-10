from machine import Pin, I2C, UART
import time

GPS = UART(1, baudrate = 9600, tx = machine.Pin(8), rx = machine.Pin(9))

try:
    while True:
        if GPS.any():
            my_char = GPS.read(1).decode('utf-8')
            print(my_char, end="")

except KeyboardInterrupt:
    print("\n Closing...")
    time.sleep(1)
    GPS.deinit()