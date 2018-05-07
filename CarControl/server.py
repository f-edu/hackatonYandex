import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 1090)
s.bind(server_address)
s.listen(1)
conn, addr = s.accept()
data=[]
while True:
    packet = conn.recv(1024)
    if not packet: break
    data.append(packet)
print(data)
conn.close()

