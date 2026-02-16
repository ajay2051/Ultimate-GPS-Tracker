from platform import machine

from machine import Pin, I2C, UART
import time
import _thread

data_lock = _thread.allocate_lock()

keep_running = True

GPS = UART(1, baudrate=9600, tx=machine.Pin(8), rx=machine.Pin(9))

NMEAdata = {
    'GPGGA': "",
    'GPGSA': "",
    'GMRMC': "",
    'GPVTG': ""
}

gps_data = {
    'latitude_decimal_degrees': 0,
    'longitude_decimal_degrees': 0,
    'heading': 0,
    'fix': False,
    'satellites': 0,
    'knots': 0
}

def gps_thread():
    print("Thread Running...")
    global keep_running, GPS, NMEAdata
    GPGGA = ""
    GPGSA = ""
    GPRMC = ""
    GPVTG = ""

    while not GPS.any():
        pass

    while GPS.any():
        junk = GPS.read()
        print(junk)
    my_NMEA = ""
    while keep_running:
        if GPS.any():
            my_char = GPS.read(1).decode('utf-8')
            my_NMEA += my_char
            if my_char == "\n":
                my_NMEA = my_NMEA.strip()
                if my_NMEA[1:6] == "GPGGA":
                    GPGGA = my_NMEA
                if my_NMEA[1:6] == "GPGSA":
                    GPGSA = my_NMEA
                if my_NMEA[1:6] == "GPRMC":
                    GPRMC = my_NMEA
                if my_NMEA[1:6] == "GPVTG":
                    GPVTG = my_NMEA
                if GPGGA != "" and GPGSA != "" and GPRMC != "" and GPVTG != "":
                    data_lock.acquire()
                    NMEAdata = {
                        'GPGGA': GPGGA,
                        'GPGSA': GPGSA,
                        'GPRMC': GPRMC,
                        'GPVTG': GPVTG
                    }
                    data_lock.release()
                my_NMEA = ""
    print("Thread Stopped...")

def parse_gps():
    try:
        gpgga = NMEA_main['GPGGA'].split(',')
        gprmc = NMEA_main['GPRMC'].split(',')

        read_fix = gpgga[6]

        if read_fix != '0' and read_fix != '':
            print("Read Fix:", read_fix)
            gps_data['fix'] = True

            # -----------------
            # Latitude (GPGGA)
            # -----------------
            latitude_raw = gpgga[2]
            if latitude_raw:
                lat_degrees = int(latitude_raw[0:2])
                lat_minutes = float(latitude_raw[2:])
                latitude_decimal_degrees = lat_degrees + (lat_minutes / 60)

                if gpgga[3] == "S":
                    latitude_decimal_degrees = -latitude_decimal_degrees

                gps_data['latitude_decimal_degrees'] = latitude_decimal_degrees

            # -----------------
            # Longitude (GPGGA)
            # -----------------
            longitude_raw = gpgga[4]
            if longitude_raw:
                lon_degrees = int(longitude_raw[0:3])
                lon_minutes = float(longitude_raw[3:])
                longitude_decimal_degrees = lon_degrees + (lon_minutes / 60)

                if gpgga[5] == "W":
                    longitude_decimal_degrees = -longitude_decimal_degrees

                gps_data['longitude_decimal_degrees'] = longitude_decimal_degrees

            # -----------------
            # Heading (GPRMC)
            # -----------------
            if gprmc[8]:
                gps_data['heading'] = float(gprmc[8])

            # -----------------
            # Speed in knots (GPRMC)
            # -----------------
            if gprmc[7]:
                gps_data['knots'] = float(gprmc[7])

            # -----------------
            # Satellites (GPGGA)
            # -----------------
            if gpgga[7]:
                gps_data['satellites'] = int(gpgga[7])

        else:
            gps_data['fix'] = False

    except (KeyError, ValueError, IndexError):
        gps_data['fix'] = False


_thread.start_new_thread(gps_thread, ())
time.sleep(2)

try:
    while True:
        data_lock.acquire()
        NMEA_main = NMEAdata.copy()
        data_lock.release()
        parse_gps()
        if gps_data['fix'] == False:
            print("Waiting for fix..")
        if gps_data['fix'] == True:
            print("Ultimate GPS Tracker Report")
            print("Latitude and Longitude", gps_data['latitude_decimal_degrees'], gps_data['longitude_decimal_degrees'])
        time.sleep(1)

except KeyboardInterrupt:
    print("\nClosing...")
    keep_running = False
    time.sleep(1)
    GPS.deinit()
    time.sleep(1)
    print("Thread Stopped...")
