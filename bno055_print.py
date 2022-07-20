# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT


import machine
import time
from bno055 import *

# fr the LCD
import lcd_rgb

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
        az_list.append(sensor.euler[0])
        alt_list.append(sensor.euler[2])
        cnt += 1

    return sum(az_list) / n, sum(alt_list) / n


def serial_out(sensor):
    print('X:', sensor.euler[0], '  Y:', sensor.euler[1], '  Z:', sensor.euler[2])


def to_dms_str(az, alt):
    m = "' "
    s = '" '

    az_dms = decdeg2dms(az)
    az_str = str(round(az_dms[0])) + " " + str(round(az_dms[1])) + m + str(az_dms[2]) + s

    alt_dms = decdeg2dms(alt)
    alt_str = str(round(alt_dms[0])) + " " + str(round(alt_dms[1])) + m + str(round(alt_dms[2], 1)) + s

    return az_str, alt_str


if __name__ == "__main__":

    while True:
        serial_out(sensor)

        # average the values before displaying
        az, alt = average(sensor)

        # change to deg min and sec
        print(az, alt)
        az_str, alt_str = to_dms_str(az, alt)

        nl = "\n"

        lcd_rgb.show(az_str + nl + alt_str)
        print(az_str + nl + alt_str)