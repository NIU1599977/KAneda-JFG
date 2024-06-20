import numpy as np
from mpu6050 import mpu6050
import time

# Inicializar el sensor
sensor = mpu6050(0x68)

def collect_static_data(sensor, num_samples=100):
    gyro_data = []
    accel_data = []
    
    for _ in range(num_samples):
        gyro_data.append(sensor.get_gyro_data()['x'])
        accel_data.append(sensor.get_accel_data()['y'])  # Usamos 'y' como ejemplo
        
        time.sleep(0.01)
    
    return np.array(gyro_data), np.array(accel_data)


def collect_movement_data(sensor, duration=10):
    gyro_data = []
    accel_data = []
    
    start_time = time.time()
    while time.time() - start_time < duration:
        gyro_data.append(sensor.get_gyro_data()['x'])
        accel_data.append(sensor.get_accel_data()['y'])  # Usamos 'y' como ejemplo
        
        time.sleep(0.01)
    
    return np.array(gyro_data), np.array(accel_data)

gyro_data, accel_data = collect_static_data(sensor)

# Calcular la varianza de los datos recolectados
gyro_var = np.var(gyro_data)
accel_var = np.var(accel_data)

print(f"Varianza del giroscopio: {gyro_var}")
print(f"Varianza del acelerómetro: {accel_var}")


time.sleep(5)

gyro_data, accel_data = collect_movement_data(sensor)

# Calcular la varianza de los datos recolectados durante el movimiento
gyro_var_movement = np.var(gyro_data)
accel_var_movement = np.var(accel_data)

print(f"Varianza del giroscopio durante movimiento: {gyro_var_movement}")
print(f"Varianza del acelerómetro durante movimiento: {accel_var_movement}")

