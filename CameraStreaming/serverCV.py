import socket, pickle
import cv2 as cv
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 1095)
s.bind(server_address)

s.listen(1)

while True:
    conn, addr = s.accept()
    # print ('Connected by', addr)
    data = []
    while True:
        packet = conn.recv(64)
        if not packet: break
        data.append(packet)
    data_arr = pickle.loads(b"".join(data))


    data_arr=cv.resize(data_arr,(200,200))
    cv.imshow("result",data_arr)

    key=cv.waitKey(1)
    data_arr=[]
    if key == ord('q'):
        s.close()
        break


    # print (data_arr)
    # conn.close()