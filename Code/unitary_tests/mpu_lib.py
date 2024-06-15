from mpu6050 import mpu6050

mpu = mpu6050(0x68)
print(mpu.read_gyro_range())
#mpu.set_gyro_range(mpu.GYRO_SCALE_MODIFIER_250DEG)
#print(mpu.get_temp())
while True:
	gyro_data = mpu.get_gyro_data()
	print('Gx: ', gyro_data['x'])
	print('Gy: ', gyro_data['y'])
	print('Gz: ', gyro_data['z'])
	accel_data = mpu.get_accel_data()
	print('Ax: ', accel_data['x'])
	print('Ay: ', accel_data['y'])
	print('Az: ', accel_data['z'])
