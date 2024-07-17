from mpu import imu
from machine import Pin, I2C

i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
imu = imu.MPU6050(i2c)

while True:
    ax = round(imu.accel.x, 2)
    ay = round(imu.accel.y, 2)
    az = round(imu.accel.z, 2)
    gx = round(imu.gyro.x)
    gy = round(imu.gyro.y)
    gz = round(imu.gyro.z)
    tem = round(imu.temperature, 2)
    print("ax", ax, "\t", "ay", ay, "\t", "az", az, "\t",
          "gx", gx, "\t", "gy", gy, "\t", "gz", gz, "\t",
          "Temperature", tem, "        ", end="\r")
