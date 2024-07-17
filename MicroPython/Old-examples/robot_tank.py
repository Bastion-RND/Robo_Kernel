from machine import Pin, PWM, I2C
from VL53L0X import VL53L0X
from time import sleep

class Chassis:
    def __init__(self, motor_pins, speed):
        self.right_back_motor_control_1 = PWM(motor_pins[0], freq=10000)
        self.right_back_motor_control_2 = PWM(motor_pins[1], freq=10000)
        
        self.left_back_motor_control_1 = PWM(motor_pins[2], freq=10000)
        self.left_back_motor_control_2 = PWM(motor_pins[3], freq=10000)
                
        self.right_forw_motor_control_1 = PWM(motor_pins[4], freq=10000)
        self.right_forw_motor_control_2 = PWM(motor_pins[5], freq=10000)
        
        self.left_forw_motor_control_1 = PWM(motor_pins[6], freq=10000)
        self.left_forw_motor_control_2 = PWM(motor_pins[7], freq=10000)        

        self.speed_rb = speed[0]
        self.speed_lb = speed[1]
        self.speed_rf = speed[2]
        self.speed_lf = speed[3]
        
    def low_stop(self):
        print('Low stop')
        self.right_back_motor_control_1.duty_u16(0)
        self.right_back_motor_control_2.duty_u16(0)
        self.left_back_motor_control_1.duty_u16(0)
        self.left_back_motor_control_2.duty_u16(0)
        self.right_forw_motor_control_1.duty_u16(0)
        self.right_forw_motor_control_2.duty_u16(0)
        self.left_forw_motor_control_1.duty_u16(0)
        self.left_forw_motor_control_2.duty_u16(0)
    
    def stop(self):
        print('Stop')
        self.right_back_motor_control_1.duty_u16(10000)
        self.right_back_motor_control_2.duty_u16(10000)
        self.left_back_motor_control_1.duty_u16(10000)
        self.left_back_motor_control_2.duty_u16(10000)
        self.right_forw_motor_control_1.duty_u16(10000)
        self.right_forw_motor_control_2.duty_u16(10000)
        self.left_forw_motor_control_1.duty_u16(10000)
        self.left_forw_motor_control_2.duty_u16(10000)
        
    def forward(self):
        print('Move forward')
        self.right_back_motor_control_1.duty_u16(self.speed_r)
        self.right_back_motor_control_2.duty_u16(0)
        self.left_back_motor_control_1.duty_u16(self.speed_l)
        self.left_back_motor_control_2.duty_u16(0)
        self.right_forw_motor_control_1.duty_u16(self.speed_r)
        self.right_forw_motor_control_2.duty_u16(0)
        self.left_forw_motor_control_1.duty_u16(self.speed_l)
        self.left_forw_motor_control_2.duty_u16(0)

    
    def back(self):
        print('Move back')
        self.right_back_motor_control_1.duty_u16(0)
        self.right_back_motor_control_2.duty_u16(self.speed_r)
        self.left_back_motor_control_1.duty_u16(0)
        self.left_back_motor_control_2.duty_u16(self.speed_l)
        self.right_forw_motor_control_1.duty_u16(0)
        self.right_forw_motor_control_2.duty_u16(self.speed_r)
        self.left_forw_motor_control_1.duty_u16(0)
        self.left_forw_motor_control_2.duty_u16(self.speed_l)
    
    
    def turnLeft(self):
        print('Turning Left')
        self.right_back_motor_control_1.duty_u16(self.speed_r)
        self.right_back_motor_control_2.duty_u16(0)
        self.left_back_motor_control_1.duty_u16(0)
        self.left_back_motor_control_2.duty_u16(self.speed_l)
        self.right_forw_motor_control_1.duty_u16(self.speed_r)
        self.right_forw_motor_control_2.duty_u16(0)
        self.left_forw_motor_control_1.duty_u16(0)
        self.left_forw_motor_control_2.duty_u16(self.speed_l)
    
    def turnRight(self):
        print('Turning Right')
        self.right_back_motor_control_1.duty_u16(0)
        self.right_back_motor_control_2.duty_u16(self.speed_r)
        self.left_back_motor_control_1.duty_u16(self.speed_l)
        self.left_back_motor_control_2.duty_u16(0)
        self.right_forw_motor_control_1.duty_u16(0)
        self.right_forw_motor_control_2.duty_u16(self.speed_r)
        self.left_forw_motor_control_1.duty_u16(self.speed_l)
        self.left_forw_motor_control_2.duty_u16(0)
        
    def set_speed(self, new_speed):
        self.speed_r = new_speed[0]
        self.speed_l = new_speed[1]
        
class Sensors:
    def __init__(self, i2c, multiplexor_adress, sensors_adress):
        self.multiplexor = multiplexor_adress
        self.i2c = i2c
        
        self.tof0_adr, self.tof1_adr, self.tof2_adr, self.tof3_adr = sensors_adress
        
        self.i2c.writeto(multiplexor_adress, self.tof0_adr)
        self.tof0 = VL53L0X(i2c)
        self.tof0.set_measurement_timing_budget(40000)
        self.tof0.set_Vcsel_pulse_period(self.tof0.vcsel_period_type[0], 12)
        self.tof0.set_Vcsel_pulse_period(self.tof0.vcsel_period_type[1], 8)
        
        self.i2c.writeto(multiplexor_adress, self.tof1_adr)
        self.tof1 = VL53L0X(i2c)
        self.tof1.set_measurement_timing_budget(40000)
        self.tof1.set_Vcsel_pulse_period(self.tof1.vcsel_period_type[0], 12)
        self.tof1.set_Vcsel_pulse_period(self.tof1.vcsel_period_type[1], 8)
        
        self.i2c.writeto(multiplexor_adress, self.tof2_adr)
        self.tof2 = VL53L0X(i2c)
        self.tof2.set_measurement_timing_budget(40000)
        self.tof2.set_Vcsel_pulse_period(self.tof2.vcsel_period_type[0], 12)
        self.tof2.set_Vcsel_pulse_period(self.tof2.vcsel_period_type[1], 8)
        
        self.i2c.writeto(multiplexor_adress, self.tof3_adr)
        self.tof3 = VL53L0X(i2c)
        self.tof3.set_measurement_timing_budget(40000)
        self.tof3.set_Vcsel_pulse_period(self.tof3.vcsel_period_type[0], 12)
        self.tof3.set_Vcsel_pulse_period(self.tof3.vcsel_period_type[1], 8)
        
    def tof0read(self):
            self.i2c.writeto(self.multiplexor, self.tof0_adr)
            return (self.tof0.ping()-50)
        
    def tof1read(self):
            self.i2c.writeto(self.multiplexor, self.tof1_adr)
            return (self.tof1.ping()-50)
        
    def tof2read(self):
            self.i2c.writeto(self.multiplexor, self.tof2_adr)
            return (self.tof2.ping()-50)
        
    def tof3read(self):
            self.i2c.writeto(self.multiplexor, self.tof3_adr)
            return (self.tof3.ping()-50)
#         
def medianaFilter(data):
    mediana = data[:]
    mediana.sort()
    return mediana[1]