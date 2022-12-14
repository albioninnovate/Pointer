#import ast
import uasyncio
import utime

"""
This version of the client script works with an earlier version of the system.  That architecture had a 
raspberrypi-server with circuit-python runsecrets.pyninng on the PICO version of the system.  This script ran on 
the laptop along with animate-polar.py. and/or stelcom.py. it function was to receive the data sent by the 
raspberry pi server which had a serial connection to the PICO. 

"""


async def tcp_echo_client(message):
    # reader, writer = await asyncio.open_connection('169.254.162.167', 8888)
    # reader, writer = await asyncio.open_connection('triscopepi.local', 8888)

    reader, writer = await uasyncio.open_connection('devpi.local', 8888)

    writer.write(message.encode())

    utime.sleep(0.2)  # allow time for the data to be received
    # n = 1000 #  works but slow
    n = 100
    data = await reader.read(n)

    writer.close()

    # data is received as a binary from which the dictionary must be extracted
    try:
 #       data_dict = ast.literal_eval(data.decode())  # extract the dictionary from the string received
        data_dict = data
        pass

    except Exception as e:
        print(e)
        data_dict = {}

    return data_dict


def main():
    received = uasyncio.run(tcp_echo_client('data pls, Thk you'))
    uasyncio.sleep(1)

    print('received by client')
    return received

if __name__ == '__main__':
    print(main())