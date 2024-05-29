from datetime import datetime
import threading
from time import sleep
#Existe una librería para la mpu6050 para la raspberry pi, quizás es util
from mpu6050 import mpu6050
import numpy as np 
from kalman import Kalman 
from moto import Moto
import math
def main():
    my_mpu = mpu6050(0x68) # Initialize MPU to get acceleration and rotation data
    My_Mpu = Kalman(my_mpu) # Object for getting theta and theta_dot


    t_init = datetime.now() # Time now

    sleep(0.5)

    print("Starting the system..!!!")
    motoClass = Moto()
    
    while 1:
        t_now = datetime.now()
        dt = (t_now - t_init).total_seconds()*1000 #Time in millis
        if dt> 0:
            aa, bb = My_Mpu.get_angle(units = 'deg')
            print("Theta [deg] = ", int(aa)," Theta_dot [deg/s] = ", int(bb), " loop time[ms] = ", np.round(dt, 2))
            motoClass.move_volanteInercia(aa, math.radians(bb)) 
#            print("hola2")
        t_init = t_now

if __name__ == '__main__':
    main()
