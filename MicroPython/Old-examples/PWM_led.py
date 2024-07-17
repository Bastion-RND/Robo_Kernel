from machine import Pin, PWM
import utime

led = PWM(Pin(25))
led.freq(1000)     
led_value = 0       
led_speed = 1

while True:
    
    led_value += led_speed           
    led.duty_u16(int(led_value * 500))     
    utime.sleep_ms(100)
    
    if led_value >= 100:
        
        led_value = 100
        led_speed = -1
               
    elif led_value <= 0:
        
        led_value = 0
        led_speed = 1
    
    print("ШИМ равен:", led_value)