from machine import Pin, PWM, SoftI2C
from VL53L0X import VL53L0X
from neopixel import NeoPixel


class Motor:
    def __init__(self, pins, freq=10000):
        self.pin_1 = PWM(Pin(pins[0], Pin.OUT), freq=freq)
        self.pin_2 = PWM(Pin(pins[1], Pin.OUT), freq=freq)
        self.freq = freq

    def clockwise(self, speed=6500):
        self.pin_1.duty_u16(int(speed))
        self.pin_2.duty_u16(0)

    def counterclockwise(self, speed=6500):
        self.pin_1.duty_u16(0)
        self.pin_2.duty_u16(int(speed))

    def low_stop(self):
        self.pin_1.duty_u16(0)
        self.pin_2.duty_u16(0)

    def stop(self):
        self.pin_1.duty_u16(self.freq)
        self.pin_2.duty_u16(self.freq)


class Encoder:
    def __init__(self, enc_pins):
        self.enc_A = Pin(enc_pins[0], Pin.IN)
        self.enc_B = Pin(enc_pins[1], Pin.IN)
        self.enc_B.irq(trigger=Pin.IRQ_RISING, handler=self.interrupt_handler)
        self.count = 0

    def interrupt_handler(self, pin):
        a = self.enc_A.value()
        if a == 1:
            self.count += 1
        elif a == 0:
            self.count -= 1

    def reset(self):
        self.count = 0


class ChassisUsual:
    def __init__(self, motors, encoders):
        self.motors = motors
        self.encoders = encoders

    def low_stop(self):
        for motor in self.motors:
            motor.low_stop()

    def stop(self):
        for motor in self.motors:
            motor.stop()

    def forward(self, speed=None):
        self.motors[0].counterclockwise(6000 if speed is None else speed[0])
        self.motors[1].counterclockwise(6000 if speed is None else speed[1])
        self.motors[2].clockwise(6000 if speed is None else speed[2])
        self.motors[3].clockwise(6000 if speed is None else speed[3])

    def back(self, speed=None):
        self.motors[0].clockwise(6000 if speed is None else speed[0])
        self.motors[1].clockwise(6000 if speed is None else speed[1])
        self.motors[2].counterclockwise(6000 if speed is None else speed[2])
        self.motors[3].counterclockwise(6000 if speed is None else speed[3])

    def turn_left(self, speed=None):
        self.motors[0].counterclockwise(6000 if speed is None else speed[0])
        self.motors[1].counterclockwise(6000 if speed is None else speed[1])
        self.motors[2].counterclockwise(6000 if speed is None else speed[2])
        self.motors[3].counterclockwise(6000 if speed is None else speed[3])

    def turn_right(self, speed=None):
        self.motors[0].clockwise(6000 if speed is None else speed[0])
        self.motors[1].clockwise(6000 if speed is None else speed[1])
        self.motors[2].clockwise(6000 if speed is None else speed[2])
        self.motors[3].clockwise(6000 if speed is None else speed[3])

    def encoders_counters(self):
        return [encoder.count for encoder in self.encoders]

    def reset_encoders(self):
        for encoder in self.encoders:
            encoder.reset()


class ChassisMecanum(ChassisUsual):
    def __init__(self, motors, encoders):
        super().__init__(motors, encoders)
        self.motors = motors

    def left(self, speed=None):
        self.motors[0].counterclockwise(5500 if speed is None else speed[0])
        self.motors[1].clockwise(5500 if speed is None else speed[1])
        self.motors[2].counterclockwise(5500 if speed is None else speed[2])
        self.motors[3].clockwise(5500 if speed is None else speed[3])

    def right(self, speed=None):
        self.motors[0].clockwise(5500 if speed is None else speed[0])
        self.motors[1].counterclockwise(5500 if speed is None else speed[1])
        self.motors[2].clockwise(5500 if speed is None else speed[2])
        self.motors[3].counterclockwise(5500 if speed is None else speed[3])

    def up_left_right(self, speed=None):
        self.motors[0].counterclockwise(5500 if speed is None else speed[0])
        self.motors[1].low_stop()
        self.motors[2].low_stop()
        self.motors[3].clockwise(5500 if speed is None else speed[3])

    def up_right_left(self, speed=None):
        self.motors[0].low_stop()
        self.motors[1].counterclockwise(5500 if speed is None else speed[1])
        self.motors[2].clockwise(5500 if speed is None else speed[2])
        self.motors[3].low_stop()

    def down_left_right(self, speed=None):
        self.motors[0].clockwise(5500 if speed is None else speed[0])
        self.motors[1].low_stop()
        self.motors[2].low_stop()
        self.motors[3].counterclockwise(5500 if speed is None else speed[3])

    def down_right_left(self, speed=None):
        self.motors[0].low_stop()
        self.motors[1].clockwise(5500 if speed is None else speed[1])
        self.motors[2].counterclockwise(5500 if speed is None else speed[2])
        self.motors[3].low_stop()


class ChassisOmni(ChassisUsual):
    def __init__(self, motors, encoders):
        super().__init__(motors, encoders)
        self.motors = motors

    def forward(self, speed=None):
        self.motors[0].low_stop()
        self.motors[1].counterclockwise(7000 if speed is None else speed[1])
        self.motors[2].clockwise(7000 if speed is None else speed[2])

    def back(self, speed=None):
        self.motors[0].low_stop()
        self.motors[1].clockwise(7000*0.9 if speed is None else speed[1])
        self.motors[2].counterclockwise(7000*1.1 if speed is None else speed[2])

    def turn_left(self, speed=None):
        self.motors[0].counterclockwise(7000*0.75 if speed is None else speed[0])
        self.motors[1].counterclockwise(7000*0.75 if speed is None else speed[1])
        self.motors[2].counterclockwise(7000*0.75 if speed is None else speed[2])

    def turn_right(self, speed=None):
        self.motors[0].clockwise(7000*0.75 if speed is None else speed[0])
        self.motors[1].clockwise(7000*0.75 if speed is None else speed[1])
        self.motors[2].clockwise(7000*0.75 if speed is None else speed[2])

    def left(self, speed=None):
        self.motors[0].counterclockwise(7000*1.6 if speed is None else speed[0])
        self.motors[1].clockwise(7000*0.88 if speed is None else speed[1])
        self.motors[2].clockwise(7000*1.08 if speed is None else speed[2])

    def right(self, speed=None):
        self.motors[0].clockwise(7000*1.2 if speed is None else speed[0])
        self.motors[1].counterclockwise(7000*0.88 if speed is None else speed[1])
        self.motors[2].counterclockwise(7000*1.08 if speed is None else speed[2])


class Sensors:
    multiplexor_address = 0x70
    sensor_address = 0x29
    sensors_addresses = {
        0: b'\x01',
        1: b'\x02',
        2: b'\x04',
        3: b'\x08',
        4: b'\x80',
        5: b'\x40',
        6: b'\x20',
        7: b'\x10'}

    def __init__(self, i2c_pins, config):
        self.config = config
        self.i2c = SoftI2C(scl=Pin(i2c_pins.get("SCL")),
                           sda=Pin(i2c_pins.get("SDA")),
                           freq=100000)

        self.sensors = None
        if self.multiplexor_address not in self.i2c.scan():
            return
        self.sensors = []

        for i in range(8):
            if int(bin(self.config)[2], 2):
                self.i2c.writeto(self.multiplexor_address, self.sensors_addresses[i])
                if self.sensor_address in self.i2c.scan():
                    self.sensors.append(VL53L0X(self.i2c))
                    self.sensors[i].set_measurement_timing_budget(40000)
                    self.sensors[i].set_Vcsel_pulse_period(self.sensors[i].vcsel_period_type[0], 12)
                    self.sensors[i].set_Vcsel_pulse_period(self.sensors[i].vcsel_period_type[1], 8)
                else:
                    self.sensors.append(None)
            else:
                self.sensors.append(None)
            self.config = self.config >> 1

    def sensors_get_values(self):
        if self.sensors is None:
            return
        data = []
        for i in range(8):
            if self.sensors[i] is not None:
                data.append(self.sensor_read(i))
            else:
                data.append(0)
        return data

    def sensor_read(self, num):
        self.i2c.writeto(self.multiplexor_address, self.sensors_addresses[num])
        return self.sensors[num].ping() - 50


class Robot:
    chassis_config = {
        "USUAL": 4,
        "MECANUM": 4,
        "TANK": 4,
        "OMNI": 3,
    }

    motor_pins = {
        0: [9, 8],
        1: [7, 6],
        2: [13, 12],
        3: [11, 10],
    }

    encoder_pins = {
        0: [26, 27],
        1: [22, 23],
        2: [20, 21],
        3: [18, 19],
    }

    i2c_pins = {
        "SCL": 2,
        "SDA": 3
    }

    button_pins = {
        25: "LEFT",
        24: "RIGHT",
    }

    leds_pins = {
        22: "RGB",
        23: "LED"
    }

    def __init__(self, config="USUAL", sensors=0xC2):
        self.config = config
        self._chassis_init()

        self.sensors_config = sensors
        self._sensors_init()

        self.buttons = []
        self._buttons_init()

        self.leds = []
        self._leds_init()

    def _chassis_init(self):
        count = self.chassis_config.get(self.config)
        self.motors = [Motor(self.motor_pins.get(i)) for i in range(count)]
        self.encoders = [Encoder(self.encoder_pins.get(i)) for i in range(count)]
        if self.config == "TANK" or self.config == "USUAL":
            self.chassis = ChassisUsual(self.motors, self.encoders)
        elif self.config == "MECANUM":
            self.chassis = ChassisMecanum(self.motors, self.encoders)
        elif self.config == "OMNI":
            self.chassis = ChassisOmni(self.motors, self.encoders)

    def _sensors_init(self):
        self.tof_sensors = Sensors(self.i2c_pins, self.sensors_config)

    def _buttons_init(self):
        for i in self.button_pins.keys():
            self.buttons.append(Pin(i, Pin.IN, Pin.PULL_UP))
        for button in self.buttons:
            button.irq(trigger=Pin.IRQ_RISING, handler=self.button_handler)

    def button_handler(self, pin):
        print(self.button_pins.get(pin), "button pressed")

    def _leds_init(self):
        for i in self.leds_pins.keys():
            if self.leds_pins.get(i) == "RGB":
                self.leds.append(NeoPixel(Pin(i), 1))
            elif self.leds_pins.get(i) == "LED":
                self.leds.append(Pin(i, Pin.OUT))


def mediana_filter(data):
    result = []
    if data is not None:
        for i in range(len(data[0])):
            mediana = [d[i] for d in data]
            mediana.sort()
            result.append(mediana[len(data)//2])
    return result

