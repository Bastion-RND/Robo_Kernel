from machine import SoftI2C, Pin
from VL53L0X import VL53L0X

sensors = [0, 0, 0, 0, 0, 0, 0, 0]

i2c = SoftI2C(sda=Pin(2), scl=Pin(3))

# disable all 8 channels
i2c.writeto(0x70, b'\x00')
print(i2c.scan())

i2c.writeto(0x70, b'\x01')
tof0 = VL53L0X(i2c)
tof0.set_measurement_timing_budget(40000)
tof0.set_Vcsel_pulse_period(tof0.vcsel_period_type[0], 12)
tof0.set_Vcsel_pulse_period(tof0.vcsel_period_type[1], 8)

i2c.writeto(0x70, b'\x02')
tof1 = VL53L0X(i2c)
tof1.set_measurement_timing_budget(40000)
tof1.set_Vcsel_pulse_period(tof1.vcsel_period_type[0], 12)
tof1.set_Vcsel_pulse_period(tof1.vcsel_period_type[1], 8)

i2c.writeto(0x70, b'\x20')
tof7 = VL53L0X(i2c)
tof7.set_measurement_timing_budget(40000)
tof7.set_Vcsel_pulse_period(tof7.vcsel_period_type[0], 12)
tof7.set_Vcsel_pulse_period(tof7.vcsel_period_type[1], 8)

while True:
    i2c.writeto(0x70, b'\x01')
    sensors[0] = tof0.ping()-50
    
    i2c.writeto(0x70, b'\x02')
    sensors[1] = tof1.ping()-50

    i2c.writeto(0x70, b'\x20')
    sensors[7] = tof7.ping()-50
    
    print(sensors)
