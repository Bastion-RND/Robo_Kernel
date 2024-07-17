from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(23))
pwm.freq(50000)

while True:
    for duty in range(50000):
        pwm.duty_u16(duty)
        sleep(0.0001)
    for duty in range(50000, 0, -1):
        pwm.duty_u16(duty)
        sleep(0.0001)
