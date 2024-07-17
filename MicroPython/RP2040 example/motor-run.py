from machine import Pin, PWM
from time import sleep

Motor1 = PWM(Pin(10))
Motor2 = PWM(Pin(11))

# STOP
Motor1.freq(8128)
Motor2.freq(8128)

# TURNING ONE WAY
Motor1.duty_u16(8128)
Motor2.duty_u16(0)

sleep(2)

# TURNING OTHER WAY
Motor1.duty_u16(0)
Motor2.duty_u16(8128)

# LOW_STOP
Motor1.freq(8128)
Motor2.freq(8128)

