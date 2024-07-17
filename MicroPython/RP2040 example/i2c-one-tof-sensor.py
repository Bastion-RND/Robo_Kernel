from VL53L0X import VL53L0X
from machine import I2C, Pin

I2C_bus = I2C(1, sda=Pin(2), scl=Pin(3))
tof = VL53L0X(I2C_bus)
tof.set_measurement_timing_budget(40000)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)

while True:
    distance = tof.ping() - 50
    if distance >= 100:
        print("WARNING! obstacle detected")
        
    if distance <= 100:
        print("OKAY")

    print(distance)
