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


_thread.start_new_thread(gps_thread, ())

try:
    while True:
        data_lock.acquire()
        NMEA_main = NMEAdata.copy()
        data_lock.release()
        print(NMEA_main['GPGGA'])
        time.sleep(1)

except KeyboardInterrupt:
    print("\nClosing...")
    keep_running = False
    time.sleep(1)
    GPS.deinit()
    time.sleep(1)
    print("Thread Stopped...")
