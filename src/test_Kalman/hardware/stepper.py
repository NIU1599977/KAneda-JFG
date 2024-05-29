"""
Archivo de configuración y declaración de funciones del Stepper 28BYJ-48.
"""
import RPi.GPIO as GPIO
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
        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

    def move(self, iterations=512, speed_time=0.00059):
        GPIO.setmode(GPIO.BOARD)
        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
            
        for i in range(iterations):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(self.control_pins[pin], HALFSTEP_SEQ[halfstep][pin])
                time.sleep(speed_time)
        GPIO.cleanup()
