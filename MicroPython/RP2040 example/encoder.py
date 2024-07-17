from machine import Pin
import utime


def interrupt_handler(self, pin):
    global direction
    a = self.enc_A.value()
    if a == 1:
        self.count += 1
        direction = "Вперед"
    elif a == 0:
        self.count -= 1
        direction = "Назад"


enc_A = Pin(26, Pin.IN)
enc_B = Pin(27, Pin.IN)
enc_B.irq(trigger=Pin.IRQ_RISING, handler=interrupt_handler)
count = 0
direction = "Вперед"

while True:

    print("Кол-во тиков : ", count, "     |   Направление : ", direction)
    utime.sleep_ms(1)