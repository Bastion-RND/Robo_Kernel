import machine
import utime
import _thread

led1 = machine.Pin(16, machine.Pin.OUT)
led2 = machine.Pin(15, machine.Pin.OUT)
sLock = _thread.allocate_lock()

def CoreTask():
    
    while True:
        
        sLock.acquire()
        print("Входим во второй тред")
        utime.sleep(1)
        led2.high()
        print("Включаем светодиод")
        utime.sleep(2)
        led2.low()
        print("Выключаем светодиод")
        utime.sleep(1)
        print("Выходим из второго треда")
        utime.sleep(1)
        sLock.release()
        
_thread.start_new_thread(CoreTask, ())

while True:
    
    sLock.acquire()
    print("Вход в основной поток") 
    led1.toggle()
    utime.sleep(0.15)
    print("Моргаем светодиодом")
    utime.sleep(1)  
    print("Выходим из основного потока") 
    utime.sleep(1)
    sLock.release()