import socket

s = socket.socket()
s.connect(('localhost', 1090))
s.send(b'hello, world!')
s.close()
