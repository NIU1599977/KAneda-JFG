from kalman_test import kalman
from src.moto import Moto
import threading
from time import sleep

def main():
    motoClass = Moto()
    movimiento_robot = threading.Thread(target=motoClass.seguir_ruta, args=())
    kalmanCode = threading.Thread(target=kalman, args=(motoClass,))
    
    kalmanCode.start()
    sleep(5) # Cada vez tarda lo que le apetece
    movimiento_robot.start()

    movimiento_robot.join()
    kalmanCode.join()
    

if __name__ == '__main__':
    main()
