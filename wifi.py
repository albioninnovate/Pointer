## wifi.py


import time
import machine
import rp2
import network
import ubinascii

import apoint
import secrets

def wlan_setup():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Comment out for powersaving mode
    wlan.config(pm=0xa11140)

    # See the MAC address in the wireless chip OTP
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    print('mac : ' + mac)


    # Other things to query
    print('WiFI channel : ', wlan.config('channel'))
    print('SSID : ', wlan.config('essid'))
    print('WiFI tx  power : ', wlan.config('txpower'))

    return wlan



def logon(wlan, ssid, password):

    wlan.connect(ssid, password)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

def blink(num_blinks, lenght_of_blink=.2):
    # Define blinking function for onboard LED to indicate error codes
    led = machine.Pin('LED', machine.Pin.OUT)

    for i in range(num_blinks):
        led.on()
        time.sleep(lenght_of_blink)
        led.off()
        time.sleep(lenght_of_blink)

    # Handle connection error
    # Error meanings
    # 0  Link Down
    # 1  Link Join
    # 2  Link NoIp
    # 3  Link Up
    # -1 Link Fail
    # -2 Link NoNet
    # -3 Link BadAuth

def main():
    blink(1,5)

    wlan = wlan_setup()

    networks = secrets.wifi_networks()

    for key in networks:
        print(key)
        ssid = key
        password = networks[key]

        logon(wlan, ssid, password)
        blink(wlan.status())

if __name__ == "__main__":
    main()