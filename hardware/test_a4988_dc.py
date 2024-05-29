import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)

for i in range(10):
  GPIO.output(8, GPIO.LOW)
  GPIO.output(10, GPIO.HIGH)
  time.sleep(5)
  GPIO.output(8, GPIO.HIGH)
  GPIO.output(10, GPIO.LOW)
  time.sleep(5)

GPIO.cleanup()