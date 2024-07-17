# More details can be found in TechToTinker.blogspot.com 
# George Bantique | tech.to.tinker@gmail.com

from VL53L0X import VL53L0X
from machine import I2C
from machine import Pin
from time import ticks_ms
import neopixel
import time

np = neopixel.NeoPixel(machine.Pin(22), 8)
brightness=10                                
colors=[[brightness,0,0],                    #red
        [0,brightness,0],                    #green
        [0,0,brightness],                    #blue
        [brightness,brightness,brightness],  #white
        [0,0,0]]                             #close

I2C_bus = I2C(1, sda=Pin(2), scl=Pin(3))
tof = VL53L0X(I2C_bus)
timer_start = ticks_ms()
timer_per = 500

while True:
    tof.start()
    distance = tof.read()
    tof.stop()
    print(distance)
    
    if ticks_ms() - timer_start >= timer_per:
        for i in range(0,5):
            for j in range(0,8):
                np[j]=colors[i]
                np.write()
                time.sleep_ms(50)
        timer_start = ticks_ms()
        
