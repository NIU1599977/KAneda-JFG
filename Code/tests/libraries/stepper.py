"""
Archivo de configuración y declaración de funciones del Stepper 28BYJ-48.
"""
import RPi.GPIO as GPIO
import sys
import time

HALFSTEP_SEQ_REV = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

HALFSTEP_SEQ = [
  [1,0,0,1],
  [0,0,0,1],
  [0,0,1,1],
  [0,0,1,0],
  [0,1,1,0],
  [0,1,0,0],
  [1,1,0,0],
  [1,0,0,0]
]

class Stepper:
    def __init__(self, control_pins):
        GPIO.setmode(GPIO.BOARD)
        self.control_pins = control_pins
        self.forward = HALFSTEP_SEQ
        self.reverse = HALFSTEP_SEQ_REV
        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

    def move(self, direction, iterations=512, speed_time=0.00059):
        GPIO.setmode(GPIO.BOARD)
        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        for i in range(iterations):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(self.control_pins[pin], direction[halfstep][pin])
                time.sleep(speed_time)
        GPIO.cleanup()

def test():
    test_stepper = Stepper([31,33,35,37])
    test_stepper.move(test_stepper.forward)
    time.sleep(0.5)
    test_stepper.move(test_stepper.reverse)
    time.sleep(0.5)

if len(sys.argv) == 2:
    if sys.argv[1] == '-t':
        test()