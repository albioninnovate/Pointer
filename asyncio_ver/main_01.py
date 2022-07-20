#import ast
import uasyncio
import utime
import network


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

async def tcp_echo_client(message):
    # reader, writer = await asyncio.open_connection('169.254.162.167', 8888)
    # reader, writer = await asyncio.open_connection('triscopepi.local', 8888)

    reader, writer = await uasyncio.open_connection('devpi.local', 8888)

    writer.write(message.encode())

    utime.sleep(.2)  # allow time for the data to be received
    # n = 1000 #  works but slow
    n = 100
    data = await reader.read(n)
    #print(data)
    writer.close()
    reader.close()
    # data is received as a binary from which the dictionary must be extracted
    try:
#        data_dict = ast.literal_eval(data.decode())  # extract the dictionary from the string received
         data_dict = data
         #print(data_dict["Y"])

    except Exception as e:
        print(e)
        data_dict = {}

    finally:
        pass
        # writer.close()
        # reader.close()


    return data_dict


def main():
    received = uasyncio.run(tcp_echo_client('data pls, Thk you'))
    print('received by client')
    utime.sleep(2)
    return received


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            pass
    #print(main())