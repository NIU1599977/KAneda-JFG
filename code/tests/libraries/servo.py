"""
Archivo de configuración y declaración de funciones del servo micro-motor SG90.
"""
from gpiozero import Servo
from time import sleep
 
class Servo_3003:
    def __init__(self, pin):
        self.servo = Servo(pin)

    def test(self):
        self.left()
        
        self.mid()

        self.right()

        self.mid()

    def mid(self):
        if (self.servo.value == 1.0):
            self.servo.min()
        else:
            self.servo.max()
        sleep(0.3)

    def right(self):
        self.servo.max()
        sleep(0.5)

    def left(self):
        self.servo.min()
        sleep(0.5)
    
    def detach(self):
        self.servo.detach()


if __name__ == "__main__":
    servo = Servo_3003(9)
    servo.test()
    # print(servo.value)
    # print(servo.max_pulse_width)
    # print(servo.min_pulse_width)
    # print(servo.pulse_width)

    # sleep(4)
    servo.detach()