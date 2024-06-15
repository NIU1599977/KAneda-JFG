import libraries.servo as servo
import libraries.stepper as stepper
import math
import smbus
import time
import RPi.GPIO as GPIO
import numpy as np

LOOP_TIME = 10
GYRO_AMOUNT = 0.996
SPEED = 10
TURN_TIME = 0.01

#IBT_2
RPWM = 12
LPWM = 32
L_EN = 8
R_EN = 10
FREQ_IBT = 100

#POLOLU
MAX_ANG = 136 # ???
#MAX_RPM = 1300
MAX_RPM = 50
class Moto:
    def __init__(self):
        self.s1 = stepper.Stepper([31,33,35,37])
        self.servo = servo

        GPIO.setmode(GPIO.BOARD)
        #IBT_2
        GPIO.setup(RPWM, GPIO.OUT)
        GPIO.setup(LPWM, GPIO.OUT)
        GPIO.setup(L_EN, GPIO.OUT)
        GPIO.setup(R_EN, GPIO.OUT)
        self.rpwm = GPIO.PWM(RPWM, FREQ_IBT)
        self.lpwm = GPIO.PWM(LPWM, FREQ_IBT)
        GPIO.output(L_EN, GPIO.HIGH)
        GPIO.output(R_EN, GPIO.HIGH)

        self.rpwm.start(0)
        self.lpwm.start(0)


        # Configuración inicial del PID
        self.kp = 0.1  # Constante proporcional
        self.ki = 0.01  # Constante integral
        self.kd = 0.001  # Constante derivativa
        self.error_anterior = 0
        self.integral = 0

    
        
    def distance_to_steps(self, distance_mm, step_angle=5.625, reduction_ratio=64, lead_screw_pitch=1):
        # Pasos por vuelta del motor sin reducción
        steps_per_revolution_motor = int(360 / step_angle)
        
        # Pasos por vuelta del eje de salida del motor con reducción
        steps_per_revolution_output = steps_per_revolution_motor * reduction_ratio
        
        # Número de vueltas necesarias para mover la distancia deseada
        turns_needed = distance_mm / lead_screw_pitch
        
        # Número de pasos necesarios
        steps_needed = int(turns_needed * steps_per_revolution_output)
        
        return steps_needed

    def calcular_pasos(distancia_mm, radio_mm=10):
        # Ángulo necesario en radianes
        angulo_rad = distancia_mm / radio_mm

        # Convertir a grados
        angulo_grados = angulo_rad * (180 / 3.14159)

        # Número de pasos en modo medio paso (0.7° por paso)
        pasos_medio_paso = angulo_grados / 0.7

        return int(pasos_medio_paso)

        
    def seguir_ruta(self):
        movimientos = [[512, 0], [100, 0.5], [512, 0]]
        for elemento in movimientos:
            iteraciones = elemento[0]
            angulo = elemento[1]
            
            #self.servo.value = angulo;
            
            time.sleep(0.5)

            if iteraciones > 0:
                self.s1.move(self.s1.forward, iteraciones)
            elif iteraciones < 0:
                aux = -1 * iteraciones
                self.s1.move(self.s1.reverse, aux)
            time.sleep(1)


    
        
    def move_volanteInercia(self, angulo, bb, dt):
        # K1 = 45
        # K2 = 30
        K1 = 500
        K2 = 40
        # GPIO.output(L_EN, GPIO.HIGH)
        # GPIO.output(R_EN, GPIO.HIGH)


        # print("Angulo [deg] = ", int(angulo)," Velocidad angular [deg/s] = ", int(dc), " loop time[ms] = ", np.round(dt, 2))
        
        if (angulo != 0):
            dc = min(100, abs(K1 * (angulo/100) + K2 * (bb/100)))
            # actual_rpm = math.fabs((bb / 360.0) * 60) # Conversión de deg/s -> rpm
            # dc = (actual_rpm / MAX_RPM) * 100
            # dc = max(30, min(100, dc_uncontrolled))
            print("dc: ", dc)
            if (angulo > 0): #Voy a asumir que cuando es > 0 se inclina a la derecha               
                self.lpwm.stop()
                self.rpwm.start(dc)

            else: #Se está inclinando hacia la izquierda, asumo
                self.rpwm.stop()
                self.lpwm.start(dc)
            
        #GPIO.output(L_EN, GPIO.LOW)
        #GPIO.output(R_EN, GPIO.LOW)
