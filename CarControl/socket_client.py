import socket
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the CarControl is listening
server_address = ('localhost', 1081)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

