import smbus2 as smbus
import RPi.GPIO as GPIO
import time
import numpy
import functions
import pickle

PWM_1 = 9
DIR_1 = 7
PWM_2 = 10
DIR_2 = 5

ENC_1 = 2
ENC_2 = 3

BRAKE = 8
BUZZER = 12
VBAT = A7

STEERING_MAX = 350
SPEED_MAX= 80
STEERING_CENTER = 1500
ST_LIMIT = 5
SPEED_LIMIT = 4

Gyro_amount = 0.996



vertical = False
calibrating = False
calibrated = False

K1 = 115;
K2 = 15.00;
K3 = 8.00;
K4 = 0.60;
loop_time = 10;

class OffsetsObj:
    def __init__(self):
        self.ID = 0
        self.AcY = 0
        self.AcZ = 0
offsets = OffsetsObj()

alpha = 0.4

AcY = numpy.int16
AcZ = numpy.int16
GyX = numpy.int16
gyroX = numpy.int16
gyroXfilt = numpy.int16

AcYc = numpy.int16
AcZc = numpy.int16
GyX_offset = numpy.int16(0)
GyX_offset_sum = numpy.int16(0)

robot_angle = 0.0
Acc_angle = 0.0

pos = numpy.int8
motor_counter = 0
enc_count = 0
motor_speed = numpy.int16
motor_pos = numpy.int32
sterring_remote = 0
speed_remote = 0
speed_value = 0
steering_value = STEERING_CENTER

bat_divider = 58 # Este valor necesita ajustarse para medir correctamente el voltaje de la batería

currentT = 0
previousT = 0
previousT_2 = 0


def save_offsets(offsets):
    with open('offsets.pickle', 'wb') as f:
        pickle.dump(offsets, f)

def load_offsets():
    with open('offsets.pickle', 'rb') as f:
        return pickle.load(f)


def setup():
    # Configuración de pines GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(DIR_2, GPIO.OUT)
    GPIO.setup(BRAKE, GPIO.OUT)
    GPIO.setup(BUZZER, GPIO.OUT)
    GPIO.setup(ENC_1, GPIO.IN)
    GPIO.setup(ENC_2, GPIO.IN)

    functions.Motor1_control(0)
    functions.Motor2_control(0)

    GPIO.add_event_detect(ENC_1, GPIO.BOTH, callback=functions.ENC_READ)
    GPIO.add_event_detect(ENC_2, GPIO.BOTH, callback=functions.ENC_READ)

    offsets = load_offsets()
    calibrated = offsets["ID"] == 35
    time.sleep(3)
    functions.beep()
    functions.angle_setup()






