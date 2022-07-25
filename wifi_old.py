import time
import machine
import rp2
import network
import ubinascii

"""
This script establishes a WIFI connection from a PICOW board#
WIFI network credentials are stored in module called secrets.py
The import module approach is used because micropython does not yet include configparser

Operation: 

on power to the PICOW Board
    1) The LED will turn on for 5 seconds to indicate the start
    2) If the REPL is open there wil be indications of various Wlan config status parameters
    3) If a WLAN is not connected, credentials will be imported from secrets.py and log in attempted
    4) After trying all the credentials the LED will flash according to the Wlan status, can take at least 10-20 seconds
    5) 3 flashes indicates connection established, any other number of flashes indicate connection not established  

    The script will only cycle trough the available SSID/password credential once and stop.  
    to try more times, power cycle.
"""


# flash indicate start of script
led = machine.Pin('LED', machine.Pin.OUT)
led.on()
time.sleep(5)
led.off()

# Set country to avoid possible errors
rp2.country('GB')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

#Comment out for powersaving mode
wlan.config(pm=0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
print('mac : ' + mac)

# Other things to query
print('WiFI channel : ', wlan.config('channel'))
print('SSID : ', wlan.config('essid'))
print('WiFI tx  power : ', wlan.config('txpower'))

# Load login data from different file for security reasons
wlan_status = wlan.status()

if wlan_status != 3:
    wlan.disconnect()
    import secrets

    networks = secrets.wifi_networks()

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