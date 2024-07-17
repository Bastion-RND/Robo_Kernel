from machine import Pin
import utime

outA = Pin(29, mode=Pin.IN)
outB = Pin(28, mode=Pin.IN)

counter = 0 
direction = "" 
outA_last = 0 
outA_current = 0 

outA_last = outA.value() 

def encoder(pin):

    global counter
    global direction
    global outA_last
    global outA_current
    
    outA_current = outA.value()
    
    if outA_current != outA_last:

        if outB.value() != outA_current:
            
            counter += 1
            direction = "Вперед"
            
        else:
            
            counter -= 1
            direction = "Назад"
        
        print("Кол-во тиков : ", counter, "     |   Направление : ",direction)
        print("\n")

    outA_last = outA_current
    utime.sleep_ms(1) 
                         
outA.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING,
              handler = encoder)
