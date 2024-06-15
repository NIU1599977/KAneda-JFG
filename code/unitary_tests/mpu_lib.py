from mpu6050 import mpu6050

mpu = mpu6050(0x68)
print("Gyro range: ", mpu.read_gyro_range())

while True:
	gyro_data = mpu.get_gyro_data()
	print('Gx: ', gyro_data['x'])
	print('Gy: ', gyro_data['y'])
	print('Gz: ', gyro_data['z'])
	accel_data = mpu.get_accel_data()
	print('Ax: ', accel_data['x'])
	print('Ay: ', accel_data['y'])
	print('Az: ', accel_data['z'])
