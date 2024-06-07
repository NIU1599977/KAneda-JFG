"""
Archivo de configuración y declaración de funciones del servo micro-motor SG90.
"""
import gpiozero
from gpiozero import Servo
from time import sleep
 
GPIO = 9

servo = Servo(GPIO, -1, 0.00049, 0.002, 0.02, gpiozero.pins.pigpio.PiGPIOFactory())
print(servo.value)

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

def turn(value):
    servo.value = value


servo.mid()
