from datetime import datetime
import threading
from time import sleep
from mpu6050 import mpu6050
import RPi.GPIO as GPIO

from libraries.kalman import Kalman 
from src.moto import Moto


def main():
    my_mpu = mpu6050(0x68) # Initialize MPU to get acceleration and rotation data
    My_Mpu = Kalman(my_mpu) # Object for getting theta and theta_dot
    t_init = datetime.now() # Time now

    sleep(0.5)


    print("Starting the system..!!!")
    motoClass = Moto()
    try:
        while 1:
            t_now = datetime.now()
            dt = (t_now - t_init).total_seconds()*1000 #Time in millis
            if dt > 0:
                motoClass.move_volanteInercia(My_Mpu, dt)
                #volante_inercia = threading.Thread(target=motoClass.move_volanteInercia, args=(My_Mpu, dt))
                #volante_inercia.start()
            t_init = t_now
            #sleep(0.003) #https://github.com/NischalSehrawat/Self-Balancing-Segway-Robot, subirlo para ver si se vuelve más estable
    except KeyboardInterrupt:
        GPIO.cleanup()
    

if __name__ == '__main__':
    main()