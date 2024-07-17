from machine import UART, Pin
from robot import Chassis

usart_flag=0
led = Pin(23, Pin.OUT)
motors = [8, 9, 10, 11, 12, 13]
speeds = [6500, 6500, 6500]
chassis = Chassis(motors, speeds)

myUsart = UART(0, baudrate=115200, rx=Pin(1), tx=Pin(0)) #bits=8, parity=0,, stop=2

while True:
    if myUsart.any():
        if usart_flag==0:
            usart_buffer=myUsart.readline()
            usart_flag=1
            print("inputString: ",usart_buffer)
    if usart_flag==1:
        if usart_buffer == b"stop\n":
            led.value(0)
            chassis.low_stop()
            print("outputString: ", usart_buffer)
            usart_flag=0
        elif usart_buffer == b'start\n':
            led.value(1)
            chassis.forward()
            print("outputString: ", usart_buffer)
            usart_flag=0
        elif usart_buffer == b'back\n':
            chassis.back()
            print("outputString: ", usart_buffer)
            usart_flag=0
        elif usart_buffer == b'right\n':
            chassis.turnRight()
            print("outputString: ", usart_buffer)
            usart_flag=0
        elif usart_buffer == b'left\n':
            chassis.turnLeft()
            print("outputString: ", usart_buffer)
            usart_flag=0
        else:
            usart_flag=0
