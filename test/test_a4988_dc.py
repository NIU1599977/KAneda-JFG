import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

for i in range(10):
  GPIO.output(12, GPIO.LOW)
  GPIO.output(16, GPIO.HIGH)
  time.sleep(5)
  GPIO.output(12, GPIO.HIGH)
  GPIO.output(16, GPIO.LOW)
  time.sleep(5)

GPIO.cleanup()