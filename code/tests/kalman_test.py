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
    filter = Kalman(my_mpu, True) # Object for getting theta and theta_dot
    t_init = datetime.now() # sTime now

    sleep(0.1)

    print("Starting the system..!!!")

    try:
        while True:
            t_now = datetime.now()
            dt = (t_now - t_init).total_seconds() #Time in seconds
            # Obtener datos del kalman
            angle_estimated, angular_velocity_estimated = filter.get_angles(dt)   
            # angle_estimated, angular_velocity_estimated = filter.get_angle(dt, 'deg')

            # Imprime o utiliza el estado estimado

            dc = motoClass.move_volanteInercia(angle_estimated, angular_velocity_estimated)
            
            print(f"Angle: {np.round(angle_estimated, 2)}, Angular Velocity: {np.round(angular_velocity_estimated, 2)}, dt: {np.round(dt, 2)}, dc: {np.round(dc, 2)}")

            t_init = t_now
            # Pausar para simular el intervalo de tiempo (ejemplo: 10 ms)
            sleep(0.01) 

    except KeyboardInterrupt:
        GPIO.cleanup()
    

kalman(Moto())