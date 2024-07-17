from machine import UART, Pin
from RoboLib import Robot

robot = Robot("TANK", 0x00)
myUsart = UART(0, 115200, rx=Pin(1), tx=Pin(0))
usart_buffer = ''

while True:
    if myUsart.any():
        usart_buffer = myUsart.read(3)
    if usart_buffer == b's\n':
        print("Stop")
        robot.chassis.stop()
    elif usart_buffer == b'f\n':
        print("Forward")
        robot.chassis.forward()
    elif usart_buffer == b'b\n':
        print("Back")
        robot.chassis.back()
    elif usart_buffer == b'r\n':
        print("Right")
        robot.chassis.right()
    elif usart_buffer == b'l\n':
        print("Left")
        robot.chassis.left()
    else:
        continue

