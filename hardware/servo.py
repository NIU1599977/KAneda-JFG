"""
Archivo de configuración y declaración de funciones del servo micro-motor SG90.
"""
from gpiozero import Servo
from time import sleep
 
GPIO = 17

servo = Servo(GPIO)

def test():
    while True:
        servo.mid()
        sleep(0.5)
        servo.min()
        sleep(0.5)
        servo.mid()
        sleep(0.5)
        servo.max()
        sleep(0.5)
        servo.value = 0.5

test()