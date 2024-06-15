from datetime import datetime
import threading
import numpy as np
from time import sleep
from mpu6050 import mpu6050
import RPi.GPIO as GPIO

from libraries.kalman import Kalman 
from libraries.remrc_balancing import Remrc
from src.moto import Moto


def kalman():
    my_mpu = mpu6050(0x68) # Initialize MPU to get acceleration and rotation data
    My_Mpu = Kalman(my_mpu) # Object for getting theta and theta_dot
    t_init = datetime.now() # Time now

    sleep(0.1)

    print("Starting the system..!!!")
    motoClass = Moto()
    try:
        while 1:

            t_now = datetime.now()
            dt = (t_now - t_init).total_seconds()*1000 #Time in millis
            if dt > 0:
                units = 'deg'
                angulo, dc = My_Mpu.get_angle(units) # bb -> velocidad angular a la que debe girar el motor

                print("Angulo [deg] = ", angulo," Velocidad angular [deg/s] = ", int(dc), " loop time[ms] = ", np.round(dt, 2))
                motoClass.move_volanteInercia(angulo, dc, dt)
                #volante_inercia = threading.Thread(target=motoClass.move_volanteInercia, args=(My_Mpu, dt))
                #volante_inercia.start()
            t_init = t_now
            sleep(0.1) #https://github.com/NischalSehrawat/Self-Balancing-Segway-Robot, subirlo para ver si se vuelve más estable
    except KeyboardInterrupt:
        GPIO.cleanup()
    

kalman()