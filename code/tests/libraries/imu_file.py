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

class mpu6050:
    def init(self, addr):
        self.bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
        self.bus.write_byte_data(DEVICE_ADDR, SMPLRT_DIV, 7)     # Write to sample rate register
        self.bus.write_byte_data(DEVICE_ADDR, PWR_MGMT_1, 1)     # Write to power management register
        self.bus.write_byte_data(DEVICE_ADDR, CONFIG, 0)         # Write to Configuration register
        self.bus.write_byte_data(DEVICE_ADDR, GYRO_CONFIG, 24)   # Write to Gyro configuration register
        self.bus.write_byte_data(DEVICE_ADDR, INT_ENABLE, 1)     # Write to interrupt enable register

    def read_raw_data(self, addr):
        # Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(DEVICE_ADDR, addr)
        low = self.bus.read_byte_data(DEVICE_ADDR, addr+1)

        # Concatenate higher and lower value
        value = ((high << 8) | low)
        
        # Get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value
    
    def get_accel_data(self):
        # Read Accelerometer raw value
        acc_x = self.read_raw_data(ACCEL_XOUT_H)
        acc_y = self.read_raw_data(ACCEL_YOUT_H)
        acc_z = self.read_raw_data(ACCEL_ZOUT_H)
        # Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0
        return {"x": Ax, "y": Ay, "z": Az}
    
    def get_accel_data(self):
        # Read Accelerometer raw value
        gyro_x = self.read_raw_data(GYRO_XOUT_H)
        gyro_y = self.read_raw_data(GYRO_YOUT_H)
        gyro_z = self.read_raw_data(GYRO_ZOUT_H)
        # Full scale range +/- 250 degree/C as per sensitivity scale factor
        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0
        return {"x": Gx, "y": Gy, "z": Gz}

