import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
from time import sleep
from datetime import datetime

class Kalman:
    
    def __init__(self, mpu):
        self.error = [0.3, -0.75, -2.45]
        gyro_var, accel_var = self.calibration_imu(mpu)
        self.kf = KalmanFilter(dim_x=2, dim_z=2)
        
        # Matriz de transición del estado
        dt = 0.01  # Intervalo de tiempo (ejemplo: 10 ms)
        self.kf.F = np.array([[1, dt],
                        [0, 1]])
        
        # Matriz de observación
        self.kf.H = np.array([[1, 0],
                        [0, 1]])
        
        # Matriz de covarianza del proceso
        q_var = 0.006  # Varianza del proceso
        self.kf.Q = Q_discrete_white_noise(dim=2, dt=dt, var=q_var)
        
        # Matriz de covarianza de la observación
        r_var = 0.03  # Varianza de la observación
        self.kf.R = np.array([[r_var, 0],
                        [0, r_var]])
        
        # Inicialización del estado
        self.kf.x = np.array([[0], [0]])
        
        # Matriz de covarianza del estado inicial
        self.kf.P = np.eye(2)
    
    def calibration_imu(self, my_mpu):
        calib = []

        print("Starting MPU calibration..."); sleep(1)
        gyro_data = []
        accel_data = []
        for i in range(100):

            xx = [my_mpu.get_accel_data()['y'], my_mpu.get_accel_data()['z'] - 9.8,
                    my_mpu.get_gyro_data()['x']]
            
            gyro_data.append(my_mpu.get_gyro_data()['x'])
            accel_data.append(my_mpu.get_accel_data()['y'])  # Usamos 'y' como ejemplo
            
            calib.append(xx)

        gyro_var = np.var(gyro_data)
        accel_var = np.var(accel_data)
            
        calib = np.array(calib) # Make is a 100*3 matrix
        
        self.error = np.mean(calib, axis = 0)
        
        print("MPU  calibrated, corrections Y, Z, Omega_x = ", round(self.error[0], 2), round(self.error[1], 2), round(self.error[2], 2))
        
        return gyro_var, accel_var


    def get_imu_data(self, my_mpu, dt):
        accel_data = my_mpu.get_accel_data()
        gyro_data = my_mpu.get_gyro_data()
        
        # Supongamos que el ángulo se obtiene integrando la velocidad angular
        # (esto es una simplificación; normalmente necesitarías un filtro complementario o algo similar)
        acc_angle = np.arctan2(accel_data['y'] - self.error[0], accel_data['z'] - self.error[1])
        angular_velocity = gyro_data['x'] - self.error[2]
        angle = angular_velocity * dt * 0.996 + acc_angle * (1.0 - 0.996)

        
        return np.array([angle, angular_velocity])