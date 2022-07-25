import socket
import machine
from bno055 import *
import wifi
import time
import network



# fr the LCD
#import lcd_rgb

"""
This script is a server running in micropython for the PICOW.  Its primary function is on connection from a client 
 is to read data from the BNO055 board via i2c and send that data to the client via a tcp socket.  

 all these need to be flashed to the PICO in addition to this script:
    bno055.py
    bno055_base.py
    secrets.py
    wifi.py

to obtain the IP address of the server to which clients can be directed, 
run with the REPL open.  The wifi module will output the IP address 
along with other wlan parameters.  

Steady 5 sec LED indicates wifi module is running.  3 quick flashes indicates connection see wifi module for more details 

There is provision for outputting the data to a LCD screen This was working under a circuit-python version  
but not tested under this micropython implementation    

"""


i2c = machine.SoftI2C(sda=machine.Pin(18), scl=machine.Pin(19), timeout=100_000)

#TODO pull wlan status from wifi model

wifi.main()

wlan = network.WLAN(network.STA_IF)

sensor = BNO055(i2c)

last_val = 0xFFFF

def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result


def decdeg2dms(dd):
    mnt, sec = divmod(dd * 3600, 60)
    deg, mnt = divmod(mnt, 60)
    return deg, mnt, sec


def average(sensor, n=100):
    cnt = 1

    az_list = []
    alt_list = []

    while cnt <= n:
        az_list.append(sensor.euler()[0])
        alt_list.append(sensor.euler()[2])
        cnt += 1

    return sum(az_list) / n, sum(alt_list) / n


def serial_out(sensor):
    print('X:', sensor.euler()[0], '  Y:', sensor.euler()[1], '  Z:', sensor.euler()[2])


def to_dms_str(az, alt):
    m = "' "
    s = '" '

    az_dms = decdeg2dms(az)
    az_dms = decdeg2dms(az)
    az_str = str(round(az_dms[0])) + " " + str(round(az_dms[1])) + m + str(az_dms[2]) + s

    alt_dms = decdeg2dms(alt)
    alt_str = str(round(alt_dms[0])) + " " + str(round(alt_dms[1])) + m + str(round(alt_dms[2], 1)) + s

    return az_str, alt_str


if __name__ == "__main__":

    # HTTP server with socket
    addr = socket.getaddrinfo('0.0.0.0', 35492)[0][-1]

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(3)

    print('Listening on', addr)

    while True:
        #serial_out(sensor)

        try:
            #print('read : ', str(sensor.euler()))
            cl, addr = s.accept()
            #print(s.recv(1024))

            #print('Client connected from', addr)
            cl.send(str(sensor.euler()))
            wifi.blink(1,0.05)
            #print('sent : ', sensor.euler())
            cl.close()

            if not wlan.ifconfig()[0]:
           # if not status[0]:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(addr)
                s.listen(3)

        except OSError as e:
            print(e)
            cl.close()
            print('Connection closed')


        # # average the values before displaying
        # az, alt = average(sensor)
        #
        # # change to deg min and sec
        # print(az, alt)
        # az_str, alt_str = to_dms_str(az, alt)
        #
        # nl = "\n"
        #
        # #lcd_rgb.show(az_str + nl + alt_str)
        # print(az_str + nl + alt_str)