#import ast
import uasyncio
import utime
import network
import socket


# ssid = 'Makespace'
# password = 'getexc1tedandmaketh1ngs'

ssid = 'DrayTek'
password = 'ILikeCake365'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
print(ssid)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    utime.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print(status)

utime.sleep(1)

message = 'data pls, Thk you'


async def tcp_echo_client(message):
    # reader, writer = await asyncio.open_connection('169.254.162.167', 8888)
    # reader, writer = await asyncio.open_connection('triscopepi.local', 8888)

    print(socket.getaddrinfo('devpi.local', 888))
    if not uasyncio.open_connection('devpi.local', 8888):
        reader, writer = await uasyncio.open_connection('devpi.local', 8888)
        print(reader)
        print(socket.getaddrinfo('devpi.local', 888))

    try:

        writer.write(message.encode())

        utime.sleep(.2)  # allow time for the data to be received
        # n = 1000 #  works but slow
        n = 100
        data = await reader.read(n)
        #print(data)

        # data is received as a binary from which the dictionary must be extracted
#        data_dict = ast.literal_eval(data.decode())  # extract the dictionary from the string received
        data_dict = data
        print(data_dict)
        writer.close()
        reader.close()
        print(reader)


    except Exception as e:
        print(e)
        #data_dict = {}

    finally:
       # writer.close()
       # reader.close()
        utime.sleep(2)

while True:
    received = uasyncio.run(tcp_echo_client('data pls, Thk you'))


