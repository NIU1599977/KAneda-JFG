import math
import smbus
import time
import pickle
import self_balancing_bike
import RPi.GPIO as GPIO



# Crear una instancia del bus I2C
bus = smbus.SMBus(1)  # El número del bus puede variar según el modelo de Raspberry Pi

MPU6050_ADDR = 0x68         # Dirección I2C del acelerómetro
ACCEL_CONFIG = 0x1C         # Dirección de configuración del acelerómetro
GYRO_CONFIG = 0x1B          # Dirección de configuración del giroscopio

# Registros: Acelerómetro, Temperatura, Giroscopio
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
TEMP_OUT_H = 0x41
TEMP_OUT_L = 0x42
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48

PWR_MGMT_1 = 0x6B
PWR_MGMT_2 = 0x6C

accSens = 0   # 0 = 2g, 1 = 4g, 2 = 8g, 3 = 16g
gyroSens = 1  # 0 = 250rad/s, 1 = 500rad/s, 2 = 1000rad/s, 3 = 2000rad/s

def writeTo(device, address, value):
    try:
        # Iniciar la transmisión de datos
        bus.write_byte_data(device, address, value)
        time.sleep(0.1)  # Esperar un breve tiempo para asegurar la escritura
        print("Datos escritos con éxito.")
    except IOError as e:
        print(f"Error al escribir en el dispositivo: {e}")


# Define la función para guardar los offsets en un archivo
def save():
    with open('offsets.pickle', 'wb') as f:
        pickle.dump(self_balancing_bike.offsets, f)

    time.sleep(0.1)  # Retardo opcional para simular delay(100) en Arduino
    with open('offsets.pickle', 'rb') as f:
        self_balancing_bike.offsets = pickle.load(f)

    if self_balancing_bike.offsets.ID == 35:
        self_balancing_bike.calibrated = True
    self_balancing_bike.calibrating = False
    print("calibrating off")
    # beep()

"""
def beep():
    self_balancing_bike.GPIO.output(self_balancing_bike.BUZZER, self_balancing_bike.GPIO.HIGH)
    time.sleep(0.07)
    self_balancing_bike.GPIO.output(self_balancing_bike.BUZZER, self_balancing_bike.GPIO.LOW)
    time.sleep(0.08)
"""

def angle_calc():
    # Calcula el ángulo del robot utilizando los datos del acelerómetro y el giroscopio. También determina si el robot está en posición vertical
    global vertical

    bus.write_byte_data(MPU6050_ADDR, ACCEL_YOUT_H, 0)
    data = bus.read_i2c_block_data(MPU6050_ADDR, ACCEL_YOUT_H, 2)
    self_balancing_bike.AcY = data[0] << 8 | data[1]

    bus.write_byte_data(MPU6050_ADDR, ACCEL_ZOUT_H, 0)
    data = bus.read_i2c_block_data(MPU6050_ADDR, ACCEL_ZOUT_H, 2)
    self_balancing_bike.AcZ = data[0] << 8 | data[1]

    bus.write_byte_data(MPU6050_ADDR, GYRO_XOUT_H, 0)
    data = bus.read_i2c_block_data(MPU6050_ADDR, GYRO_XOUT_H, 2)
    self_balancing_bike.GyX = data[0] << 8 | data[1]

    self_balancing_bike.AcYc = self_balancing_bike.AcY - self_balancing_bike.offsets.AcY
    self_balancing_bike.AcZc = self_balancing_bike.AcZ - self_balancing_bike.offsets.AcZ
    self_balancing_bike.GyX -= self_balancing_bike.GyX_offset

    self_balancing_bike.robot_angle += self_balancing_bike.GyX * self_balancing_bike.LOOP_TIME / 1000 / 65.536
    self_balancing_bike.Acc_angle = -math.atan2(self_balancing_bike.AcYc, -self_balancing_bike.AcZc) * 57.2958
    self_balancing_bike.robot_angle = self_balancing_bike.robot_angle * self_balancing_bike.GYRO_AMOUNT + self_balancing_bike.Acc_angle * (1.0 - self_balancing_bike.GYRO_AMOUNT)

    if abs(self_balancing_bike.robot_angle) > 10:
        self_balancing_bike.vertical = False
    if abs(self_balancing_bike.robot_angle) < 0.4:
        self_balancing_bike.vertical = True

def angle_setup():
    # Configura el acelerómetro y el giroscopio y calcula el offset del giroscopio
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)
    bus.write_byte_data(MPU6050_ADDR, ACCEL_CONFIG, accSens << 3)
    bus.write_byte_data(MPU6050_ADDR, GYRO_CONFIG, gyroSens << 3)

    for i in range(1024):
        angle_calc()
        self_balancing_bike.GyX_offset_sum += self_balancing_bike.GyX
        time.sleep(0.003)

    self_balancing_bike.GyX_offset = self_balancing_bike.GyX_offset_sum >> 10
    #beep()
    #beep()
    print("GyX offset:", self_balancing_bike.GyX_offset)

def battVoltage(voltage):
    if voltage > 8 and voltage <= 9.5:
        self_balancing_bike.GPIO.output(self_balancing_bike.BUZZER, self_balancing_bike.GPIO.HIGH)
    else:
        self_balancing_bike.GPIO.output(self_balancing_bike.BUZZER, self_balancing_bike.GPIO.LOW)


#Motor1 y Motor2 controlan la velocidad y dirección de los motores del robot
def Motor1_control(sp):
    if sp > 0:
        self_balancing_bike.GPIO.output(self_balancing_bike.DIR_1, self_balancing_bike.GPIO.LOW)
    else:
        self_balancing_bike.GPIO.output(self_balancing_bike.DIR_1, self_balancing_bike.GPIO.HIGH)
    self_balancing_bike.PWM_1.start(255 - abs(sp))

def Motor2_control(sp):
    if sp > 0:
        self_balancing_bike.GPIO.output(self_balancing_bike.DIR_2, self_balancing_bike.GPIO.LOW)
    else:
        self_balancing_bike.GPIO.output(self_balancing_bike.DIR_2, self_balancing_bike.GPIO.HIGH)
    self_balancing_bike.PWM_2.start(255 - abs(sp))

def ENC_READ():
    cur = ((not GPIO.input(self_balancing_bike.ENC_1)) << 1) + (not GPIO.input(self_balancing_bike.ENC_2))
    old = self_balancing_bike.pos & 0b11
    dir = (self_balancing_bike.pos & 0b110000) >> 4

    if cur == 3: 
        cur = 2
    elif cur == 2: 
        cur = 3

    if cur != old:
        if dir == 0:
            if cur == 1 or cur == 3:
                dir = cur
        else:
            if cur == 0:
                if dir == 1 and old == 3:
                    self_balancing_bike.enc_count -= 1
                elif dir == 3 and old == 1:
                    self_balancing_bike.enc_count += 1
                dir = 0
        self_balancing_bike.pos = (dir << 4) + (old << 2) + cur