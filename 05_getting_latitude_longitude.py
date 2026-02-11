from machine import Pin, I2C, UART
import time

GPS = UART(1, baudrate=9600, tx=machine.Pin(8), rx=machine.Pin(9))
my_NMEA = ""
GPGGA = ""
GPGSA = ""
GPRMC = ""
GPVTG = ""
GPGSV = ""

while not GPS.any():
    pass
while GPS.any():
    junk = GPS.read()

try:
    while True:
        if GPS.any():
            my_char = GPS.read(1).decode('utf-8')
            my_NMEA += my_char
            if my_char == "\n":
                if my_NMEA[1:6] == "GPGGA":
                    GPGGA = my_NMEA
                    GPGGAArray = GPGGA.split(",")
                    if int(GPGGAArray[6]) != 0:
                        latitude_raw = GPGGAArray[2]
                        longitude_raw = GPGGAArray[4]
                        number_of_satellites = GPGGAArray[7]
                        latitude_decimal_degrees = int(latitude_raw[0:2]) + float(latitude_raw[2:]) / 60
                        longitude_decimal_degrees = int(longitude_raw[0:3]) + float(latitude_raw[3:]) / 60
                        if GPGGAArray[3] == 'S':
                            latitude_decimal_degrees = -latitude_decimal_degrees
                        if GPGGAArray[3] == 'W':
                            longitude_decimal_degrees = -longitude_decimal_degrees
                    print(GPGGA)
                    print(GPGGAArray)
                if my_NMEA[1:6] == "GPGSA":
                    GPGSA = my_NMEA
                    GPGSAArray = GPGSA.split(",")
                    print(GPGSA)
                    print(GPGSAArray)
                if my_NMEA[1:6] == "GPRMC":
                    GPRMC = my_NMEA
                    GPRMCArray = GPRMC.split(",")
                    knots = float(GPRMCArray[7])
                    heading = float(GPRMCArray[8])
                    print(GPRMC)
                    print(GPRMCArray)
                if my_NMEA[1:6] == "GPVTG":
                    GPVTG = my_NMEA
                    GPVTGArray = GPVTG.split(",")
                    print(GPVTG)
                    print(GPVTGArray)
                if my_NMEA[1:6] == "GPGSV":
                    GPGSV = my_NMEA
                    GPGSVArray = GPGSV.split(",")
                    print(GPGSV)
                    print(GPGSVArray)
                    if GPGGA != "":
                        if int(GPGGAArray[6]) == 0:
                            print("Acquiring Fix:", GPGSAArray[3], "Satellites in View")
                my_NMEA = ""

except KeyboardInterrupt:
    print("\n Closing...")
    time.sleep(1)
    GPS.deinit()
