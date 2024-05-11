"""
Archivo de configuración y declaración de funciones de la Unidad de Medición Inercial, 
IMU por sus siglas en inglés, MPU-6050.
"""
import smbus					# Import SMBus module of I2C
from time import sleep

# Some MPU6050 Registers and their Address
DEVICE_ADDR = 0x68
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def init():
    bus.write_byte_data(DEVICE_ADDR, SMPLRT_DIV, 7)     # Write to sample rate register
    bus.write_byte_data(DEVICE_ADDR, PWR_MGMT_1, 1)     # Write to power management register
    bus.write_byte_data(DEVICE_ADDR, CONFIG, 0)         # Write to Configuration register
    bus.write_byte_data(DEVICE_ADDR, GYRO_CONFIG, 24)   # Write to Gyro configuration register
    bus.write_byte_data(DEVICE_ADDR, INT_ENABLE, 1)     # Write to interrupt enable register

def read_raw_data(addr):
	# Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(DEVICE_ADDR, addr)
    low = bus.read_byte_data(DEVICE_ADDR, addr+1)

    # Concatenate higher and lower value
    value = ((high << 8) | low)
    
    # Get signed value from mpu6050
    if(value > 32768):
            value = value - 65536
    return value

def get_data(): # TODO: Tener en cuenta offsets
    print (" Reading Data of Gyroscope and Accelerometer")
    # Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)

    # Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    # Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax = acc_x/16384.0
    Ay = acc_y/16384.0
    Az = acc_z/16384.0

    Gx = gyro_x/131.0
    Gy = gyro_y/131.0
    Gz = gyro_z/131.0
    print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
    
    return {
        "acc_x": acc_x,
        "acc_y": acc_y,
        "acc_z": acc_z,
        "gyro_x": gyro_x,
        "gyro_y": gyro_y,
        "gyro_z": gyro_z,
        "Ax": Ax,
        "Ay": Ay,
        "Az": Az,
        "Gx": Gx,
        "Gy": Gy,
        "Gz": Gz
    }

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
init()
