from datetime import datetime
import threading
from time import sleep
#Existe una librería para la mpu6050 para la raspberry pi, quizás es util
from mpu6050 import mpu6050
import numpy as np 
from src.kalman import Kalman 

def main():
    my_mpu = mpu6050(0x68) # Initialize MPU to get acceleration and rotation data
    My_Mpu = Kalman(my_mpu) # Object for getting theta and theta_dot


    t_init = datetime.now() # Time now

    sleep(0.5)

    print("Starting the system..!!!")
    while 1:
        t_now = datetime.now()
        dt = (t_now - t_init).total_seconds()*1000 #Time in millis
        if dt> 0:
            aa, bb = My_Mpu.get_angle(units = 'deg')
            print("Theta [deg] = ", int(aa)," Theta_dot [deg/s] = ", int(bb), " loop time[ms] = ", np.round(dt, 2))
            # Si esto va, hay que mirar como mover el volante de inercia para contrarrestarlo y mantenerse en pie
            # Si aa es > o < 0 se está inclinando a un lado, por lo que hay que girar el volante hacia el otro lado
            # Tb dependiendo de la velocidad angular sabremos si se está inclinando demasiado rápido por lo que dependiendo de este valor, le daremos más caña al volante o menos caña
        t_init = t_now

if __name__ == '__main__':
    main()