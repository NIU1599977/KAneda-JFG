#https://keithweaverca.medium.com/controlling-stepper-motors-using-python-with-a-raspberry-pi-b3fbd482f886
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
control_pins = [18,22,24,26]
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
simple_seq = [
  [1,0,0,0],
  [0,1,0,0],
  [0,0,1,0],
  [0,0,0,1]
]
another_seq = [
  [1,1,0,0],
  [0,1,1,0],
  [0,0,1,1],
  [1,0,0,1]
]
halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]
fullstep_seq = [
  [1,0,0,1],
  [1,1,0,0],
  [0,1,1,0],
  [0,0,1,1]
]
for i in range(512):
  for halfstep in range(8):
    for pin in range(4):
      GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
    time.sleep(0.00059) # velocidad máxima
"""
for i in range(512):
    for step in range(4):
        for pin in range(8):
            GPIO.output(control_pins[pin], another_seq[step][pin])
        time.sleep(0.01)
"""
GPIO.cleanup()
