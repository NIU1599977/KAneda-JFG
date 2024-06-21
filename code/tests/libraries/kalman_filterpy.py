import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
from time import sleep
from datetime import datetime

class Kalman:
    
    def __init__(self, mpu, calibrate=True):
        self.error = [0.3, -0.75, -2.45]
        if calibrate:
            calib = []
            print("Starting MPU calibration..."); sleep(1)
            gyro_data = []
            accel_data = []
            for i in range(100):

                xx = [mpu.get_accel_data()['y'], mpu.get_accel_data()['z'] - 9.8,
                        mpu.get_gyro_data()['x']]
                
                calib.append(xx)

            calib = np.array(calib) # Make is a 100*3 matrix
            
            self.error = np.mean(calib, axis = 0)                
        
        print("MPU  calibrated, corrections Y, Z, Omega_x = ", round(self.error[0], 2), round(self.error[1], 2), round(self.error[2], 2))             

        print('Calculating initial conditions for Kalman filter')
        R = [] # For initial values and sensor covariance matrix
        
        for i in range(100):
            
            f1 = np.arctan((mpu.get_accel_data()['y'] - self.error[0]) / (mpu.get_accel_data()['z'] - self.error[1]))
            f2 = np.deg2rad(mpu.get_gyro_data()['x'] - self.error[2]) # Gyro bias [rad] 
            
            R.append([f1,f2]) # 100 samples of angle and angular velocity (bias in gyro) in [rad] and [rad/s] respectively
            
        R = np.array(R); # Make it an array of 100*2
       
        init_conditions = np.mean(R, axis = 0).reshape(2,1) # Get initial conditions in 2*1 form
       
        print('Calculated initial states for Kalman filter Acc angle, Gyro bias (constant inaccuracy) ', init_conditions)   
        

        self.kf = KalmanFilter(dim_x=2, dim_z=2)
        
        # Matriz de transición del estado
        dt = 0.03  # Intervalo de tiempo (ejemplo: 10 ms)
        self.kf.F = np.array([[1, -dt],
                        [0, 1]])
        
        # Matriz de observación
        self.kf.H = np.eye(2) # matriz identidad
        
        # Matriz de covarianza del proceso
        q_var = 0.006  # Varianza del proceso, si vemos que driftea mucho es porque tenemos que aumentarlo, si vemos que va muy lento es porque tenemos que bajarlo
        self.kf.Q = Q_discrete_white_noise(dim=2, dt=dt, var=q_var) # process noise covarianze matrix
        # self.Q = np.diag([0.01, 0.03]) # si va lento, hay que bajar 0.01. si driftea mucho hay que aumentar 0.03
        
        # Matriz de covarianza de la observación
        self.kf.R = 0.03  # si es muy alto, el filtro responderá muy lento ya que no tendrá en cuenta las medidas, si es muy bajo, se nos colará ruido del acelerometro
        # self.kf.R = np.array([[r_var, 0], [0, r_var]])
        
        # Inicialización del estado
        self.kf.x = init_conditions 
        
        # Matriz de covarianza del estado inicial
        self.kf.P = np.eye(2) # matriz identidad


    def get_imu_data(self, my_mpu, dt):
        accel_data = my_mpu.get_accel_data()
        gyro_data = my_mpu.get_gyro_data()
        
        # Supongamos que el ángulo se obtiene integrando la velocidad angular
        # (esto es una simplificación; normalmente necesitarías un filtro complementario o algo similar)
        acc_angle = np.rad2deg(np.arctan2(accel_data['y'] - self.error[0], accel_data['z'] - self.error[1])) # arctan devuelve en radianes
        angular_velocity = gyro_data['x'] - self.error[2] # º/s
        angle = angular_velocity * dt * 0.996 + acc_angle * (1.0 - 0.996)

        
        return np.array([angle, angular_velocity])