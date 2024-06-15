from src.moto import Moto
from Kalman_test import kalman
import threading

def main():
    motoClass = Moto()
    movimiento_robot = threading.Thread(target=motoClass.seguir_ruta, args=None)
    kalmanCode = threading.Thread(target=kalman, args=None)
    
    kalmanCode.start()
    movimiento_robot.start()

    movimiento_robot.join()
    kalmanCode.join()
    

if __name__ == '__main__':
    main()