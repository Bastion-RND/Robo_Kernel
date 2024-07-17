from VL53L0X import VL53L0X
from machine import I2C
from machine import Pin
from time import ticks_ms

I2C_bus = I2C(1, sda=Pin(2), scl=Pin(3))
tof = VL53L0X(I2C_bus)
timer_start = ticks_ms()
timer_per = 500

while True:
    tof.start()
    distance = tof.read()
    tof.stop()
    if distance >= 100:
        chassis.low_stop()
        
    if distance <= 100:
        chassis.forward()   