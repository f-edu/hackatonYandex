import cv2 as cv
import numpy as np

def labeling(identy_array,traffic_dict):

    max_element = max(identy_array)
    max_element_id = identy_array.index(max(identy_array))

    if max_element<2800:
        max_element_id="No_sign"
    return traffic_dict[max_element_id]

# Пример распознавания
def tsr_recognition(img,examples_arr,traffic_dict):
    try:
        identity_array = []
        if img.any():

            resizedRoi = cv.resize(img, (64, 64))
            thresh = cv.inRange(resizedRoi, (89, 91, 149), (255, 255, 255))


            for example in examples_arr:
                identity_sign = 0
                example = cv.inRange(example, (89, 91, 149), (255, 255, 255))
                for i in range(64):
                    for j in range(64):
                        # sign 1 recognition
                        if (thresh[i][j] == example[i][j]):
                            identity_sign += 1
                identity_array.append(identity_sign)
            label = labeling(identity_array, traffic_dict)
            return label

    except: return None
# Пример детектирования
def tsr_detection(frame):
        # Преобразование в цветовое пространство HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # cv.imshow("hsv", hsv)
        # Далее можно работать с готовым HSV или с одним из шкал (H,S или V)
        # h = hsv[:, :, 0]
        # s = hsv[:, :, 1]
        # v = hsv[:, :, 2]

        # Размытие
        blur = cv.blur(hsv, (5, 5))
        # cv.imshow("blur", blur)
        # Бинаризация по порогу
        tresh = cv.inRange(blur, (89, 124, 73), (255, 255, 255))
        # cv.imshow("tresh", tresh)
        # Эрозия и дилатация (восстановление)
        tresh = cv.erode(tresh, None, iterations=2)
        tresh = cv.dilate(tresh, None, iterations=4)
        # cv.imshow("tresh", tresh)
        # Поиск контуров на изображении
        countours = cv.findContours(tresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        countours = countours[1]
        # ib
        height,width=tresh.shape
        min_x, min_y = width, height
        max_x = max_y = 0
        roiImg = []
        for cnt in countours:
            # Сортировка контуров (поиск самого большого)
            cnt = sorted(countours, key=cv.contourArea, reverse=True)[0] # Самый большой контур

            # Выделение бокса (крайних точек изображения)
            rect = cv.minAreaRect(cnt)
            box = np.int0(cv.boxPoints(rect))
            # Отрисовка контуров на изображении
            cv.drawContours(frame, [box], -1, (0, 255, 0), 3)

            # Выделение части, на которой расположен знак из изображении
            (x, y, w, h) = cv.boundingRect(cnt)
            min_x, max_x = min(x, min_x), max(x + w, max_x)
            min_y, max_y = min(y, min_y), max(y + h, max_y)
            roiImg = frame[min_y:max_y, min_x:max_x]

        # Отображение результатов (основного фрейма)
        # cv.imshow("result", frame)

        return roiImg


def main():

    # Преобразуем примеры знаков к стандартному размеру и читаем из папки одновременно
    pedistrain = cv.resize(cv.imread("pedistrain.png"), (64, 64))
    no_drive = cv.resize(cv.imread("noDrive.png"), (64, 64))

    # Собираем массив из примеров изображений знаков
    examples_arr = [pedistrain,no_drive]
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
    # Читаем видеопоток из камеры
    cap = cv.VideoCapture(0)
    while (True):
        ret, frame = cap.read()

        # Детектируем область с предполагаемым знаком на изображении
        detect_roi=tsr_detection(frame)
        # Распознаем знак на изображении
        identity_array=tsr_recognition(detect_roi,examples_arr,traffic_dict)

        print(identity_array)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()