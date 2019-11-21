import socket
import threading

shutdown = False

host = "127.0.0.1"
port = 2002

server = (host, 2019)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

message = ''

while message != 'q':
    message = input()
    if message != '':
        s.sendto(str(message).encode(), server)

s.close()
