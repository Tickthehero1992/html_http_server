import socket
import sys
import time
HOST, PORT = "192.168.1.19", 8000
data = "".join(sys.argv[1:])
data = ":1.1,1115,1882;"
data2 = ":1.2,1115,1992;"
data3 = ":1.3,1115,1994;"
# Create a socket (SOCK_STREAM means a TCP socket)
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
    sock.send(data.encode("utf-8"))
    time.sleep(2)
    sock.send(data2.encode("utf-8"))
    time.sleep(2)
    sock.send(data3.encode("utf-8"))
    time.sleep(2)