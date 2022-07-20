import socket

picoIP = '10.0.254.252'

picoPort = 80

tcpSocket = socket.socket()

try:
    tcpSocket.connect((picoIP,picoPort))
    data = tcpSocket.recv(1024)

    print(data)

except Exception as e:
    print(e)
    tcpSocket.close()