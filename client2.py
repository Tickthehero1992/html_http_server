"""import socket
import sys
import time
HOST, PORT = "192.168.1.112", 8080
data = "".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

    # Receive data from the server and shut down
while True:
    sock.send(b"Device_1 176L/min;")
    time.sleep(3)
"""
import numpy as np
