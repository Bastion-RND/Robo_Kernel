import cv2
import numpy as np
from pygrabber.dshow_graph import FilterGraph

class object:

    # поиск желтого объекта
    """
    Каждая функция опредления цветного объекта содержит цветовой диапазон
    для того чтобы алгоритм распознавал объекты при плохом и хорошем освещении.
    Так же в каждой функции происходит вызов главной функции которая отвечает за
    сбор и обработку данных с камеры.
    """
    def find_yellow(port):
        hsv_min = np.array((0, 94, 165), np.uint8)# определяем нижнюю границу цвета
        hsv_max = np.array((255, 255, 255), np.uint8)# определяем верхнюю границу цвета
        find_object(hsv_max, hsv_min, port=port)# вызываем функцию поиска объекта
    # поиск зеленого объекта
    def find_green(port):
        hsv_min = np.array((54, 36, 0), np.uint8)
        hsv_max = np.array((111, 210, 255), np.uint8)
        find_object(hsv_max, hsv_min, port=port)
    # поиск коричневого объекта
    def find_brown(port):
        hsv_min = np.array((0, 106, 0), np.uint8)
        hsv_max = np.array((19, 210, 255), np.uint8)
        find_object(hsv_max, hsv_min, port=port)

    # поиск порта к которому подключена камера
    """
    Поиск индекса порта к которому подключены камеры реализован при помощи
    сторонней библиотеки pygrabber. Библиотека раелизована на основе OpenCV
    и предоставляет инструменты для работы с видео.
    """
    def find_port():
        devices = FilterGraph().get_input_devices()# получаем подключенные устройства

        available_cameras = {}

        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name# перебираем устройства и записываем в словарь

        print(available_cameras)
    """
    Функция масштабирования изображения реализована при помощи стандартных инструментов
    OpenCV, при помощи метода resize, которому необходимо передать изображение и 
    кортеж значений длины и высоты.
    """
    # масштабирование изображения
    def resize_image(img_path, out_path, width, height):
        img = cv2.imread(img_path)# читаем изображение
        out = cv2.resize(img, (width, height))# изменяем размер
        cv2.imwrite(out_path+f"/{str(width)}.jpg", out)# записываем изображение по указанному пути

# поиск объекта
def find_object(hsv_max, hsv_min, port = 1):
        
        # переменная cap хранит запись видео
        cap = cv2.VideoCapture(port)
        
        # бесконечный цикл для чтения видео покадрово
        while True:

            # читаем отдельные фреймы (картинки)
            frame = cap.read()
        #----------------------------------------------------------------
            # преобразуем RGB картинку в HSV модель
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # применяем цветовой фильтр
            thresh = cv2.inRange(hsv, hsv_min, hsv_max)

            result = frame.copy()
            # ищем контуры по маске
            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]

            count=[]
            coord = {}
            # перебираем найденные контуры для создания ограничивающих рамок
            for cntr in contours:
                x,y,w,h = cv2.boundingRect(cntr)
                if w*h > 300:
                # счет рамок (определение количества объектов)    
                #----------------------------------------------------------------    
                    x1=w/2
                    y1=h/2
                    cx=x+x1
                    cy=y+y1
                    count.append([cx,cy])
                #----------------------------------------------------------------
                    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # производим расчет для определения какой объект ближе
                    dist_to_corner = frame.shape[1] - h + 2*y
                    coord[dist_to_corner] = [x,y,w,h]

            if bool(coord) == True:
                min_key = max(coord.keys())
                cv2.putText(result, "nearest", (coord[min_key][0], coord[min_key][1]), 
                                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0),thickness=2)
            print("count:",len(count))
            global counter
            counter = len(count)
        #----------------------------------------------------------------
            cv2.imshow('frame', result)
            
            # записываем условие на событие нажатие q
            if cv2.waitKey(1) == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()   
