from machine import Pin


def button_handler(pin):
    global interrupt_flag
    interrupt_flag = 1


interrupt_flag=0
counter = 0
button = Pin(24, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)

while True:
    if interrupt_flag == 1:
        interrupt_flag = 0
        counter += 1
        print("Pressed {} times".format(counter))
