from machine import UART, Pin
from RoboLib import Robot, mediana_filter

usart_flag = 0
mode_flag = 0

sensors = [[0] * 8] * 5
robot = Robot("OMNI", 0xE6)
myUsart = UART(0, 115200, rx=Pin(1), tx=Pin(0))
usart_buffer = ''

while True:
    if myUsart.any():
        if usart_flag == 0:
            usart_buffer = myUsart.read(3)
            usart_flag = 1
            print("inputString: ", usart_buffer)
    if usart_flag == 1:
        if usart_buffer == b"s\n":
            robot.leds[1].value(0)
            robot.chassis.low_stop()
            print("outputString: ", usart_buffer)
            usart_flag = 0
        elif usart_buffer == b'f\n':
            robot.leds[1].value(1)
            robot.chassis.forward()
            print("outputString: ", usart_buffer)
            usart_flag = 0
        elif usart_buffer == b'b\n':
            robot.chassis.back()
            print("outputString: ", usart_buffer)
            usart_flag = 0
        elif usart_buffer == b'r\n':
            robot.chassis.turn_right()
            print("outputString: ", usart_buffer)
            usart_flag = 0
        elif usart_buffer == b'l\n':
            robot.chassis.turn_left()
            print("outputString: ", usart_buffer)
            usart_flag = 0
        elif usart_buffer == b'm\n':
            mode_flag = not mode_flag
            usart_flag = 0
            robot.chassis.low_stop()
            print("mode changed: ", mode_flag)
        else:
            usart_flag = 0

        print("mode now: ", mode_flag)

    if mode_flag:
        sensors.pop(0)
        res = robot.tof_sensors.sensors_get_values()
        for i in range(len(res)):
            if res[i] < 50:
                res[i] = sensors[-1][i]
        sensors.append(res)
        data = mediana_filter(sensors)

        print(data)

        if sensors[0][0] != 0:
            if (data[5] < 160) or (data[6] < 140):
                robot.chassis.stop()
                print('Turning Right')
                robot.chassis.turn_right()
            elif (data[2] < 140) or (data[1] < 140) or (data[0] < 160):
                robot.chassis.stop()
                print('Turning Left')
                robot.chassis.turn_left()
            else:
                robot.chassis.stop()
                print('Forward')
                robot.chassis.forward()
