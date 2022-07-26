from picorobotics import PicoRobotics
import utime
import client_pico

board = PicoRobotics.KitronikPicoRobotics()
directions = ["f","r"]

def test():
    while True:
            for direction in directions:
                 for stepcount in range(200):
                    board.step(1,direction,8)
                    board.step(2,direction,8)
            utime.sleep_ms(500)#pause between motors




if __name__ == '__main__':
    pos_start = {'az': 0.0,
                 'alt': 0.0
                 }
    pos_crnt = pos_start

    az_last = 0
    alt_last = 0



    while True:
        data = client_pico.main()
        az = data[0]
        alt = data[2]

        az_delta  = az + az_last
        alt_delta = alt + alt_last

        board.stepAngle(1,1,alt_delta,holdPosition=True)







