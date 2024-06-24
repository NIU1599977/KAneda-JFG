import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
from time import sleep
from datetime import datetime

class Kalman:
    
    def __init__(self, mpu, calibrate=True):
        self.mpu = mpu
        self.error = [0.3, -0.75, -2.45]
        self.angle = 0
        if calibrate:
            calib = []
            print("Starting MPU calibration..."); sleep(1)

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
            
            f1 = np.arctan2((mpu.get_accel_data()['y'] - self.error[0]), (mpu.get_accel_data()['z'] - self.error[1]))
            f2 = np.deg2rad(mpu.get_gyro_data()['x'] - self.error[2]) # Gyro bias [rad] 
            
            R.append([f1,f2]) # 100 samples of angle and angular velocity (bias in gyro) in [rad] and [rad/s] respectively
            
        R = np.array(R); # Make it an array of 100*2
       
        init_conditions = np.mean(R, axis = 0).reshape(2,1) # Get initial conditions in 2*1 form
       
        print('Calculated initial states for Kalman filter Acc angle, Gyro bias (constant inaccuracy) ', init_conditions)   
        

        self.kf = KalmanFilter(dim_x=2, dim_z=2)
        
        # Matriz de transición del estado
        dt = 0.02  # Intervalo de tiempo (ejemplo: 10 ms)
        self.kf.F = np.array([[1, -dt],
                        [0, 1]])
        
        # Matriz de observación
        self.kf.H = np.eye(2) # matriz identidad
        
        # Matriz de covarianza del proceso
        self.q_var = 0.003  # Varianza del proceso, si vemos que driftea mucho es porque tenemos que aumentarlo, si vemos que va muy lento es porque tenemos que bajarlo
        self.kf.Q = Q_discrete_white_noise(dim=2, dt=dt, var=self.q_var) # process noise covarianze matrix
        # self.Q = np.diag([a, b]) 
        # si angulo estimado empieza a driftear, hay que subir b.
        # si angulo estimado se actualiza lentamente hay que bajar a para hacerlo más responsivo
        
        # Matriz de covarianza de la observación
        self.kf.R = 0.05  # si es muy alto, el filtro responderá muy lento ya que no tendrá en cuenta las medidas, si es muy bajo, se nos colará ruido del acelerometro
        # self.kf.R = np.array([[r_var, 0], [0, r_var]])
        
        # Inicialización del estado
        self.kf.x = init_conditions 
        
        # Matriz de covarianza del estado inicial
        self.kf.P = np.diag([0, 0])

    def get_angles(self, dt):
        z = self.get_imu_data(dt)
        # self.kf.Q = Q_discrete_white_noise(dim=2, dt=dt, var=self.q_var) # process noise covarianze matrix
        # self.kf.F = np.array([[1, -dt], [0, 1]])
        # Predicción del estado
        self.kf.predict()
        
        # Actualización del estado con la nueva observación
        self.kf.update(z)
        angle_estimated, angular_velocity_estimated = self.kf.x
        
        return np.rad2deg(angle_estimated), np.rad2deg(angular_velocity_estimated)

    def get_imu_data(self, dt):
        accel_data = self.mpu.get_accel_data()
        gyro_data = self.mpu.get_gyro_data()
        
        # Supongamos que el ángulo se obtiene integrando la velocidad angular
        # (esto es una simplificación; normalmente necesitarías un filtro complementario o algo similar)
        alpha = 0.996
        angle = np.arctan2((accel_data['y'] - self.error[0]), accel_data['z'] - self.error[1]) # arctan devuelve en radianes
        angular_velocity = np.deg2rad(gyro_data['x'] - self.error[2]) # rad/s
        # self.angle = alpha * (angular_velocity * dt + angle) + (1 - alpha) * self.angle
        
        return np.array([self.angle, angular_velocity])