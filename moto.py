import hardware.imu.py
import hardware.servo.py
import hardware.stepper.py
import math
import smbus
import time

LOOP_TIME = 10
GYRO_AMOUNT = 0.996
SPEED = 10
TURN_TIME = 0.01

class Moto:
    def __init__(self):
        self.K1 = 0
        self.K2 = 0
        self.K3 = 0
        self.K4 = 0
        self.vertical = False
        self.angle = 0
        self.acc_angle = 0
        self.s1 = stepper.Stepper([31,33,35,37])
        self.s2 = stepper.Stepper([18,22,24,26])
        self.servo = Servo(17)

    def calibrate(): # Adaptación de Tuning() (functions.ino)
        calibrated = False
        while not calibrated:
            pisae = input("Introduce la variable a calibrar ('p','i','s','a') o 'e' si terminaste la calibración.")
            if pisae == 'p':
                accion = input("Indica + para incrementar o - para decrementar.")
                if accion == '+':
                    self.K1 += 1
                elif accion == '-':
                    self.K1 -= 1
                else:
                    print("La tecla introducida no es correcta, empiece de nuevo.")
            elif pisae == 'i':
                accion = input("Indica + para incrementar o - para decrementar.")
                if accion == '+':
                    self.K2 += 0.5
                elif accion == '-':
                    self.K2 -= 0.5
                else:
                    print("La tecla introducida no es correcta, empiece de nuevo.")
            elif pisae == 's':
                accion = input("Indica + para incrementar o - para decrementar.")
                if accion == '+':
                    self.K3 += 0.2
                elif accion == '-':
                    self.K3 -= 0.2
                else:
                    print("La tecla introducida no es correcta, empiece de nuevo.")
            elif pisae == 'a':
                accion = input("Indica + para incrementar o - para decrementar.")
                if accion == '+':
                    self.K4 += 0.05
                elif accion == '-':
                    self.K4 -= 0.05
                else:
                    print("La tecla introducida no es correcta, empiece de nuevo.")
            elif pisae == 'e':
                calibrated = True
            else:
                print("La tecla introducida no es correcta, empiece de nuevo.")
            print(f"K1: {self.K1}\nK2: {self.K2}\nK3: {self.K3}\nK4: {self.K4}")

    def angle_calc():
        acc_data = imu.get_data()
        # Revisar por posibles offsets o usar valores raw (ej. gyro_x)
        self.angle += acc_data["Gx"] * LOOP_TIME / 1000 / 65.536
        self.acc_angle = -math.atan2(acc_data["Ay"], -acc_data["Az"]) * 57.2958
        self.angle = self.angle * self.GYRO_AMOUNT + self.acc_angle * (1.0 - self.GYRO_AMOUNT)

        if abs(self.angle) > 10:
            self.vertical = False
        if abs(self.angle) < 0.4:
            self.vertical = True

    def angle_setup():
        for i in range(1024): # 1024 ?
            angle_calc()
            time.sleep(0.003)

    def enc_read(): # TODO: Entender para qué sirve esto y si hace falta (leer stepper).
        pass
        
    def move(distance, angle):
        # TODO: Pasar ángulo a valor entre 0 y 1.
        # TODO: Pasar distancia a número de iteraciones.
        move_time = abs(distance / SPEED)
        turn_time = abs(angle * TURN_TIME)
        if angle > 0:
            self.servo.turn(angle)
            time.sleep(turn_time)
        else:
            self.servo.turn(0)

        if distance > 0:
            self.s1.move(distance) # Cambiar por s2 si no es este stepper.
            time.sleep(move_time)