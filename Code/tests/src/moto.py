import HW_Code.imu_file as imu
import HW_Code.servo as servo
import HW_Code.stepper as stepper
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
FREQ_IBT = 50

#POLOLU
MAX_ANG = 136 # ???
MAX_RPM = 1300

class Moto:
    def __init__(self):
        self.K1 = 115
        self.K2 = 15.00
        self.K3 = 8.00
        self.K4 = 0.60
        self.vertical = False
        self.angle = 0.0
        self.acc_angle = 0.0
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


        # Configuración inicial del PID
        self.kp = 0.1  # Constante proporcional
        self.ki = 0.01  # Constante integral
        self.kd = 0.001  # Constante derivativa
        self.error_anterior = 0
        self.integral = 0
    
    

    def angle_calc(self):
        acc_data = imu.get_data()
        # Revisar por posibles offsets o usar valores raw (ej. gyro_x)
        self.angle += acc_data["Gx"] * LOOP_TIME / 1000 / 65.536
        self.acc_angle = -math.atan2(acc_data["Ay"], -acc_data["Az"]) * 57.2958
        self.angle = self.angle * self.GYRO_AMOUNT + self.acc_angle * (1.0 - self.GYRO_AMOUNT)

        if abs(self.angle) > 10:
            self.vertical = False
        if abs(self.angle) < 0.4:
            self.vertical = True

    def angle_setup(self):
        for i in range(1024): # 1024 ?
            self.angle_calc()
            time.sleep(0.003)

    
        
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
        distance = 5 # 5 iteraciones
        angle = 0
        iteraciones = self.distance_to_steps(distance)
        print("ITERACIONES --> ", iteraciones)
        move_time = abs(distance / SPEED)
        turn_time = abs(angle * TURN_TIME)
        if angle > 0:
            self.servo.turn(angle)
            time.sleep(turn_time)
        else:
            self.servo.turn(0)

        if distance > 0:
            self.s1.move(self.s1.forward, iteraciones, move_time) 
            time.sleep(move_time)
        
    def move_volanteInercia(self, My_Mpu, dt):
        GPIO.output(L_EN, GPIO.HIGH)
        GPIO.output(R_EN, GPIO.HIGH)
        units = 'deg'
        angulo, bb = My_Mpu.get_angle(units) # bb -> velocidad angular a la que debe girar el motor
        print("Angulo [deg] = ", int(angulo)," Velocidad angular [deg/s] = ", int(bb), " loop time[ms] = ", np.round(dt, 2))
        
        if (angulo != 0):
            actual_rpm = math.fabs((bb / 360.0) * 60) # Conversión de deg/s -> rpm
            dc = max(1.0, (actual_rpm / MAX_RPM)) * 100

            if (angulo > 0): #Voy a asumir que cuando es > 0 se inclina a la derecha               
                self.lpwm.stop()
                self.rpwm.start(dc)

            else: #Se está inclinando hacia la izquierda, asumo
                self.rpwm.stop()
                self.lpwm.start(dc)

        GPIO.output(L_EN, GPIO.LOW)
        GPIO.output(R_EN, GPIO.LOW)
