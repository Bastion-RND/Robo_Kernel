import machine

sda=machine.Pin(26)
scl=machine.Pin(27)

i2c=machine.I2C(1, sda=sda, scl=scl)

for a in range(500):
    print(i2c.scan())
