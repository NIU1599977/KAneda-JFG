from datetime import datetime
import threading
import numpy as np
from time import sleep
from mpu6050 import mpu6050
import RPi.GPIO as GPIO

from libraries.kalman_filterpy import Kalman 
# from libraries.kalman import Kalman
from src.moto import Moto


def kalman(motoClass):
    my_mpu = mpu6050(0x68) # Initialize MPU to get acceleration and rotation data
    My_Mpu = Kalman(my_mpu) # Object for getting theta and theta_dot
    dt = 0.01

    sleep(0.1)

    print("Starting the system..!!!")

    try:
        while True:
            t_now = datetime.now()
            # Obtener datos del IMU
            z = My_Mpu.get_imu_data(my_mpu, dt)
            kf = My_Mpu.kf
            # Predicción del estado
            kf.predict()
            
            # Actualización del estado con la nueva observación
            kf.update(z)
            
            # Obtén el estado estimado
            angle_estimated, angular_velocity_estimated = kf.x
            # angle_estimated, angular_velocity_estimated = My_Mpu.get_angle('deg')

            # Imprime o utiliza el estado estimado
            print(f"Angle: {angle_estimated}, Angular Velocity: {angular_velocity_estimated}")

            motoClass.move_volanteInercia(angle_estimated, angular_velocity_estimated, dt)
            
            t_init = t_now
            # Pausar para simular el intervalo de tiempo (ejemplo: 10 ms)
            sleep(0.01) 
            dt = (t_now - t_init).total_seconds()*1000 #Time in millis

    except KeyboardInterrupt:
        GPIO.cleanup()
    

kalman(Moto())