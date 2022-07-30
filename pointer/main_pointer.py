
## pointer.py

import picorobotics
# from picorobotics import PicoRobotics
import utime
from client.client_pico import get_data
import wifi

board = picorobotics.KitronikPicoRobotics()
#board = PicoRobotics.KitronikPicoRobotics()
directions = ["f","r"]

def test():
    while True:
            for direction in directions:
                 for stepcount in range(200):
                    board.step(1,direction,8)
                    board.step(2,direction,8)
            utime.sleep_ms(500)#pause between motors


if __name__ == '__main__':
    wifi.main()

    az_last = 0
    alt_last = 0

    while True:
        data = get_data()
        print('data ;' , data)
        az = data[0]
        alt = data[2]

        az_delta  = az - az_last
        alt_delta = alt - alt_last
        print('alt_delta ;', alt_delta)

        if alt_delta >= 0:
            alt_dir = 'f'
        elif alt_delta < 0:
            alt_dir = 'r'
            alt_delta = alt_delta * -1

        print('alt_dir :', alt_dir)

        board.stepAngle(2,alt_dir,alt_delta,holdPosition=False)

        alt_last = alt
        print('alt_last ;', alt_last)
        utime.sleep(1)
