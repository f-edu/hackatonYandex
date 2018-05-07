import numpy as np
import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        #Отображение текста на кадрах видеопотока (вставьте наименование знака вместо helloworld)
        ## TODO: Напишите код для детектирования и распознавания знака


        #cv2.putText(frame, "Hello world!", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        # Отображение видео (необходимо убрать при запуске по ssh):
        #cv2.imshow('frame', frame)
        out.write(frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
out.release()

cv2.destroyAllWindows()
