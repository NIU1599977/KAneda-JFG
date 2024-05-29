import RPi.GPIO as GPIO
import time

#### CÓDIGO NUEVO

GPIO.cleanup()
print("Cleaned")
time.sleep(2)

RPWN = 12
LPWN = 32
L_EN = 18
R_EN = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RPWN, GPIO.OUT) # RPWM
GPIO.setup(LPWN, GPIO.OUT) # LPWM
GPIO.setup(L_EN, GPIO.OUT) # L_EN
GPIO.setup(R_EN, GPIO.OUT) # R_EN

GPIO.output(L_EN, GPIO.HIGH) # ACTIVAR LOS DOS ENABLES
GPIO.output(R_EN, GPIO.HIGH)

frequency = 100
rpwm = GPIO.PWM(RPWN, frequency)
lpwm = GPIO.PWM(LPWN, frequency)

dutycycle = 10 #cambiar para editar la velocidad de giro

# main
print("palante")
rpwm.start(dutycycle)
time.sleep(2)
rpwm.stop()
print("patras")
lpwm.start(dutycycle)
time.sleep(2)
lpwm.stop()

GPIO.cleanup()


