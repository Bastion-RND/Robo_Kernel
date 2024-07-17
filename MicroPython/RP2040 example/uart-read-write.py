from machine import UART, Pin

myUsart = UART(0, baudrate=115200, bits=8, parity=0, rx=Pin(1), tx=Pin(0), stop=2)
myUsart.write(f"\r\nPico initialization completed!\r\n")
usart_buffer = ''

while True:
    if myUsart.any():
        usart_buffer=myUsart.read(myUsart.any())
        print(f"inputString: {usart_buffer}")
    if len(usart_buffer):
        out = input("enter your answer: ")
        print(f"ouputString: {out}")
        myUsart.write(bytes(out, 'utf-8'))
        usart_buffer = ''
              