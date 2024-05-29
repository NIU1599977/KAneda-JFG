import hardware.imu
from hardware.servo import *
from hardware.stepper import *
import threading

def main():
    s1 = Stepper([31,33,35,37])
    
    turn_value = [-1, 0, 1]
    for i in range(2):
        t1 = threading.Thread(target=turn, args=(turn_value[i],))
        t2 = threading.Thread(target=s1.move, args=(512,0.00059,))
    
        t1.start()
        t2.start()

        t1.join()
        t2.join()


if __name__ == '__main__':
    main()
