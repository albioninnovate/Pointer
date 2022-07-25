import socket

"""
This script is a client that receives data from the 
"""

picoIP = '10.0.254.252'

picoPort = 35492

tcpSocket = socket.socket()

try:
    tcpSocket.connect((picoIP,picoPort))
    data = tcpSocket.recv(100)

    print(data)

except Exception as e:
    print(e)
    tcpSocket.close()
