import rp2
import network
import ubinascii
import socket

import json

import secrets

import machine
import time
from bno055 import *

# fr the LCD
#import lcd_rgb

# Use these lines for I2C
# bno_SDA = board.GP18
# bno_SCL = board.GP19

#i2c = busio.I2C(bno_SCL, bno_SDA)
#i2c = machine.I2C(0, sda=machine.Pin(18), scl=machine.Pin(19))  # EIO error almost immediately
i2c = machine.SoftI2C(sda=machine.Pin(18), scl=machine.Pin(19), timeout=100_000)

#sensor = adafruit_bno055.BNO055_I2C(i2c)
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

    # Get online
    # Set country to avoid possible errors
    rp2.country('GB')

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # If you need to disable powersaving mode
    # wlan.config(pm = 0xa11140)

    # See the MAC address in the wireless chip OTP
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    print('mac = ' + mac)

    # Other things to query
    print('WiFI channel : ', wlan.config('channel'))
    print('SSID : ',wlan.config('essid'))
    print('WiFI tx  power : ',wlan.config('txpower'))

    # Load login data from different file for safety reasons

    # ssid = 'DrayTek'
    # password = 'ILikeCake365'

#    ssid = 'Makespace'
#    password = 'getexc1tedandmaketh1ngs'

    wlan_status = wlan.status()
    if wlan_status != 3:
        import secrets

        networks =secrets.wifi_networks()

        for key in networks:
            print(key)
            ssid = key
            password = networks[key]
            wlan.connect(ssid, password)

            # Wait for connection with 10 second timeout
            timeout = 10
            while timeout > 0:
                if wlan.status() < 0 or wlan.status() >= 3:
                    break
                timeout -= 1
                print('Waiting for connection...')
                time.sleep(1)


    # Define blinking function for onboard LED to indicate error codes
    def blink_onboard_led(num_blinks):
        led = machine.Pin('LED', machine.Pin.OUT)
        for i in range(num_blinks):
            led.on()
            time.sleep(.2)
            led.off()
            time.sleep(.2)


    # Handle connection error
    # Error meanings
    # 0  Link Down
    # 1  Link Join
    # 2  Link NoIp
    # 3  Link Up
    # -1 Link Fail
    # -2 Link NoNet
    # -3 Link BadAuth

    wlan_status = wlan.status()
    blink_onboard_led(wlan_status)

    if wlan_status != 3:
        raise RuntimeError('Wi-Fi connection failed')

    else:
        print('Connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])


    # HTTP server with socket
    addr = socket.getaddrinfo('0.0.0.0', 35492)[0][-1]

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(3)

    print('Listening on', addr)
    led = machine.Pin('LED', machine.Pin.OUT)

    while True:
        #serial_out(sensor)

        try:
            print('read : ', str(sensor.euler()))
            cl, addr = s.accept()
            #print(s.recv(1024))
            print('Client connected from', addr)
            cl.send(str(sensor.euler()))
            print('sent : ', sensor.euler())
            cl.close()
            if not status[0]:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(addr)
                s.listen(3)

        except OSError as e:
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