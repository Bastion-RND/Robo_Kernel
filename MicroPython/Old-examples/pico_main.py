from machine import UART, Pin, SoftI2C
from robot import Chassis, Sensors, medianaFilter

usart_flag=0
mode_flag = 0
led = Pin(23, Pin.OUT)
motors = [7, 6, 10, 11, 9, 8, 12, 13]
speeds = [6500, 6500]
sensors_adress = [b'\x01', b'\x02', b'\x04', b'\x08', b'\x10', b'\x20', b'\x40']
chassis = Chassis(motors, speeds)

i2c = SoftI2C(sda=Pin(3), scl=Pin(2))
multiplexor_adress = 0x70
sensors = Sensors(i2c, multiplexor_adress, sensors_adress)

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
        elif usart_buffer == b's\n':
            led.value(1)
            chassis.forward()
            print("outputString: ", usart_buffer)
            usart_flag=0
        elif usart_buffer == b'b\n':
            chassis.back()
            print("outputString: ", usart_buffer)
            usart_flag=0
        elif usart_buffer == b'r\n':
            chassis.turnRight()
            print("outputString: ", usart_buffer)
            usart_flag=0
        elif usart_buffer == b'l\n':
            chassis.turnLeft()
            print("outputString: ", usart_buffer)
            usart_flag=0
        elif usart_buffer == b'm\n':
            mode_flag != mode_flag
           
        else:
            usart_flag=0
            
        if mode_flag==1:
            if (d0 < 150) or (d1 < 150) or (d2 < 150) or (d3 < 150):
                chassis.stop()
                print('Turning Right')
                chassis.turnRight(6500)
            else:
                chassis.stop()
                print('Forward')
                chassis.forward(6500)

