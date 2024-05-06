import smbus2 as smbus
import RPi.GPIO as GPIO
import time
import numpy
import functions
import pickle
import remote
from gpiozero import Servo

# Constants declaration
HALFSTEP_SEQ = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]


PWM_1 = 9
DIR_1 = 7
PWM_2 = 10
DIR_2 = 5

ENC_1 = 2
ENC_2 = 3

BRAKE = 8
BUZZER = 12
#VBAT = A7

STEERING_MAX = 350
SPEED_MAX = 80
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
steering_remote = 0
speed_remote = 0
speed_value = 0
steering_value = STEERING_CENTER

bat_divider = 58 # Este valor necesita ajustarse para medir correctamente el voltaje de la batería

currentT = 0
previousT = 0
previousT_2 = 0
# Define el pin al que está conectado el servo
#pin_servo = 17

# Crea un objeto Servo
#steering_servo = Servo(pin_servo)

def save_offsets(offsets):
    with open('offsets.pickle', 'wb') as f:
        pickle.dump(offsets, f)

def load_offsets():
    with open('offsets.pickle', 'rb') as f:
        return pickle.load(f)


def gpio_setup():
    # Configuración de pines GPIO
    GPIO.setmode(GPIO.BOARD)

    ## Servo motor SG90
    servoGpio = 17
    sg90 = Servo(servoGpio)

    ## Stepper 28BYJ-48 (1)
    stepper1_pins = [18,22,24,26]
    for pin in stepper1_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    
    ## Stepper 28BYJ-48 (2)
    stepper2_pins = [31,33,35,37]
    for pin in stepper2_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    ## Accelerometer MPU-6050
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7) # Write to sample rate register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1) # Write to power management register
    bus.write_byte_data(Device_Address, CONFIG, 0) # Write to Configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24) # Write to Gyro configuration register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1) # Write to interrupt enable register

    functions.Motor1_control(0)
    functions.Motor2_control(0)

    GPIO.add_event_detect(ENC_1, GPIO.BOTH, callback=functions.ENC_READ)
    GPIO.add_event_detect(ENC_2, GPIO.BOTH, callback=functions.ENC_READ)

    offsets = load_offsets()
    calibrated = offsets["ID"] == 35
    time.sleep(3)
    #functions.beep()
    functions.angle_setup()

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def loop():
    currentT = time.time() * 1000

    if currentT - previousT >= loop_time:
        #Tuning()
        user_input = input("Por favor entra un comando dist y angulo de esta forma dist,ang: ")
        dist, ang = user_input.split(',')
        dist = int(x)
        ang = int(y)
        remote.move(dist, ang)
        functions.angle_calc()

        motor_speed = -enc_count
        enc_count = 0

        if vertical and calibrated and not calibrating:
            GPIO.output(BRAKE, GPIO.HIGH)
            gyroX = GyX / 131.0 # convert to deg/s
            gyroXfilt = alpha * gyroX + (1 - alpha)*gyroXfilt 
            motor_pos += motor_speed
            motor_pos = constrain(motor_pos, -110, 110)

            pwm = constrain(K1*robot_angle+K2*gyroXfilt+K3*motor_speed+K4*motor_pos, -255, 255)
            functions.Motor1_control(-pwm)

            if (speed_value - speed_remote) > SPEED_LIMIT:
                speed_value -= SPEED_LIMIT
            elif (speed_value - speed_remote) < -SPEED_LIMIT:
                speed_value += SPEED_LIMIT
            else:
                speed_value = speed_remote
            if (steering_value - STEERING_CENTER - steering_remote) > ST_LIMIT:
                steering_value -= ST_LIMIT
            elif (steering_value - STEERING_CENTER - steering_remote) < -ST_LIMIT:
                steering_value += ST_LIMIT
            else:
                steering_value = STEERING_CENTER + steering_remote

            steering_servo.value = steering_value
            functions.Motor2_control(speed_value)
        else:
            GPIO.output(BRAKE, GPIO.LOW)
            steering_value = STEERING_CENTER
            steering_servo.value = STEERING_CENTER
            speed_value = 0
            functions.Motor1_control(0)
            functions.Motor2_control(0)
            motor_pos = 0
        previousT = currentT
    if currentT - previousT_2 >= 2000:
        if not calibrated and not calibrating:
            print("first you need to calibrate the balacing point...")
        previousT_2 = currentT

def main():
    gpio_setup()
    while True:
        loop()

if __name__ == '__main__':
    main()
