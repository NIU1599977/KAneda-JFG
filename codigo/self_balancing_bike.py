import smbus2 as smbus
import RPi.GPIO as GPIO
import time
import functions
# Definición de constantes
PWM_1 = 9
DIR_1 = 7
PWM_2 = 10
DIR_2 = 5

ENC_1 = 2
ENC_2 = 3

BRAKE = 8
BUZZER = 12
VBAT = 7

STEERING_MAX = 350
SPEED_MAX = 80
STEERING_CENTER = 1500
ST_LIMIT = 5
SPEED_LIMIT = 4

GYRO_AMOUNT = 0.996

# Variables globales
vertical = False
calibrating = False
calibrated = False

K1 = 115
K2 = 15.00
K3 = 8.00
K4 = 0.60
LOOP_TIME = 10
class OffsetsObj:
    def __init__(self):
        self.ID = 0
        self.AcY = 0
        self.AcZ = 0
offsets = OffsetsObj()
alpha = 0.4

AcY = AcZ = GyX = gyroX = gyroXfilt = 0
AcYc = AcZc = 0
GyX_offset = 0
GyX_offset_sum = 0

robot_angle = 0
Acc_angle = 0

pos = 0
motor_counter = 0
enc_count = 0
motor_speed = 0
motor_pos = 0
steering_remote = 0
speed_remote = 0
speed_value = 0
steering_value = STEERING_CENTER

bat_divider = 58

currentT = previousT_1 = previousT_2 = 0

# Configuración de pines GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PWM_1, GPIO.OUT)
GPIO.setup(DIR_1, GPIO.OUT)
GPIO.setup(PWM_2, GPIO.OUT)
GPIO.setup(DIR_2, GPIO.OUT)
GPIO.setup(BRAKE, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(ENC_1, GPIO.IN)
GPIO.setup(ENC_2, GPIO.IN)
# En Raspberry Pi, no necesitas configurar los temporizadores como en Arduino
steering_servo = None  # Deberías usar la biblioteca adecuada para controlar servos en Raspberry Pi
calibrated = False


def setup():
    global calibrated
    GPIO.setup(PWM_1, GPIO.OUT)
    GPIO.setup(PWM_2, GPIO.OUT)
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(DIR_2, GPIO.OUT)
    GPIO.setup(BRAKE, GPIO.OUT)
    GPIO.setup(BUZZER, GPIO.OUT)
    GPIO.setup(ENC_1, GPIO.IN)
    GPIO.setup(ENC_2, GPIO.IN)
    
    # Cargar offsets desde la EEPROM
    offsets["ID"] = 35  # Supongamos que los offsets se cargaron correctamente
    calibrated = offsets["ID"] == 35
    time.sleep(3)  # Emular el retraso de 3 segundos
    functions.beep()  # Llamar a la función beep
    functions.angle_setup()

def loop():
    global currentT
    global previousT_1
    global previousT_2

    currentT = time.time() * 1000

    if currentT - previousT_1 >= LOOP_TIME:
        functions.readControlParameters()
        functions.angle_calc()

        motor_speed = -enc_count
        enc_count = 0

        if vertical and calibrated and not calibrating:
            functions.digitalWrite(BRAKE, HIGH)
            gyroX = GyX / 131.0

            gyroXfilt = alpha * gyroX + (1 - alpha) * gyroXfilt

            motor_pos += motor_speed
            motor_pos = constrain(motor_pos, -110, 110)

            pwm = constrain(K1 * robot_angle + K2 * gyroXfilt + K3 * motor_speed + K4 * motor_pos, -255, 255)
            functions.Motor1_control(-pwm)

            if speed_value - speed_remote > SPEED_LIMIT:
                speed_value -= SPEED_LIMIT
            elif speed_value - speed_remote < -SPEED_LIMIT:
                speed_value += SPEED_LIMIT
            else:
                speed_value = speed_remote

            if steering_value - STEERING_CENTER - steering_remote > ST_LIMIT:
                steering_value -= ST_LIMIT
            elif steering_value - STEERING_CENTER - steering_remote < -ST_LIMIT:
                steering_value += ST_LIMIT
            else:
                steering_value = STEERING_CENTER + steering_remote

            steering_servo.write(steering_value)
            functions.Motor2_control(speed_value)
        else:
            functions.digitalWrite(BRAKE, LOW)
            steering_value = STEERING_CENTER
            steering_servo.write(STEERING_CENTER)
            speed_value = 0
            functions.Motor1_control(0)
            functions.Motor2_control(0)
            motor_pos = 0

        previousT_1 = currentT

    if currentT - previousT_2 >= 2000:
        functions.battVoltage(functions.analogRead(VBAT) / bat_divider)
        if not calibrated and not calibrating:
            print("first you need to calibrate the balancing point...")
        previousT_2 = currentT

def constrain(value, min_value, max_value):
    return min(max(value, min_value), max_value)