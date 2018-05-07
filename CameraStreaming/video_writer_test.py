import numpy as np
import cv2 as cv
# import traffic_sign_recognition as tsr
import CameraStreaming.traffic_sign_recognition as tsr

import socket
import pickle

cap = cv.VideoCapture(4)

fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 30.0, (640,480))

# Преобразуем примеры знаков к стандартному размеру и читаем из папки одновременно
pedistrain = cv.resize(cv.imread("pedistrain.png"), (64, 64))
no_drive = cv.resize(cv.imread("noDrive.png"), (64, 64))

# Собираем массив из примеров изображений знаков
examples_arr = [pedistrain, no_drive]
traffic_dict = {
    "No_sign": [0, 0, 0, 0, 0, 0, 0, 0],
    0: [1, 0, 0, 0, 0, 0, 0, 0],
    1: [0, 1, 0, 0, 0, 0, 0, 0],
    2: [0, 0, 1, 0, 0, 0, 0, 0],
    3: [0, 0, 0, 1, 0, 0, 0, 0],
    4: [0, 0, 0, 0, 1, 0, 0, 0],
    5: [0, 0, 0, 0, 0, 1, 0, 0],
    6: [0, 0, 0, 0, 0, 0, 1, 0],
    7: [0, 0, 0, 0, 0, 0, 0, 1]
}
result_dict = {
    "Нет занка": [0, 0, 0, 0, 0, 0, 0, 0],
    "pedistrain": [1, 0, 0, 0, 0, 0, 0, 0],
    "no_drive": [0, 1, 0, 0, 0, 0, 0, 0],
    "stop": [0, 0, 1, 0, 0, 0, 0, 0],
    "way_out": [0, 0, 0, 1, 0, 0, 0, 0],
    "no_entry": [0, 0, 0, 0, 1, 0, 0, 0],
    "road_works": [0, 0, 0, 0, 0, 1, 0, 0],
    "parking": [0, 0, 0, 0, 0, 0, 1, 0],
    "a_unevenness": [0, 0, 0, 0, 0, 0, 0, 1]
}

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
def send_data(roi):
    HOST = '172.24.1.85'
    PORT = 1090
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    img = roi
    data_string = pickle.dumps(img)
    s.send(data_string)
    s.close()

# def socket_send(string):
#
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # server_address = ('localhost', 1086)
#     server_address = ('localhost', 1094) #raspberry
#
#     sock.connect(server_address)
#
#     try:
#         # Отправка данных
#         message = string.encode()
#         sock.sendall(message)
#
#     finally:
#         sock.close()


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        #Отображение текста на кадрах видеопотока (вставьте наименование знака вместо helloworld)
        ## TODO: Напишите код для детектирования и распознавания знака
        roi=tsr.tsr_detection(frame)
        try:


            identity_array = tsr.tsr_recognition(roi, examples_arr, traffic_dict)
            # print(identity_array)
            res=get_key(result_dict,identity_array)


            roi=cv.resize(roi,(20,20))

            if res !="Нет занка":
                print(res)
                cv.putText(frame, res, (10, 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
                cv.putText(roi, res, (4, 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)
                try:
                    send_data(roi)
                except:pass
            # cv.imshow("roi", roi)
        except: pass

        # cv.putText(frame, "Hello world!", (20, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        # Отображение видео (необходимо убрать при запуске по ssh):
        # cv.imshow('frame', frame)
        out.write(frame)


        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
out.release()

cv.destroyAllWindows()


