import math
import smbus
import time
import pickle
import self_balancing_bike

# Dirección del dispositivo I2C
DEVICE_ADDRESS = 0x68  # Ejemplo de dirección, asegúrate de ajustarla según tu dispositivo

# Crear una instancia del bus I2C
bus = smbus.SMBus(1)  # El número del bus puede variar según el modelo de Raspberry Pi

MPU6050 = 0x68              # Dirección del dispositivo
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
        pickle.dump(offsets, f)

    time.sleep(0.1)  # Retardo opcional para simular delay(100) en Arduino
    with open('offsets.pickle', 'rb') as f:
        offsets = pickle.load(f)

    if offsets.ID == 35:
        calibrated = True
    calibrating = False
    print("calibrating off")
    beep()

def beep():
    self_balancing_bike.GPIO.output(self_balancing_bike.BUZZER, self_balancing_bike.GPIO.HIGH)
    time.sleep(0.07)
    self_balancing_bike.GPIO.output(self_balancing_bike.BUZZER, self_balancing_bike.GPIO.LOW)
    time.sleep(0.08)

def angle_calc():
    global vertical

    bus.write_byte_data(MPU6050, ACCEL_YOUT_H, 0)
    data = bus.read_i2c_block_data(MPU6050, ACCEL_YOUT_H, 2)
    AcY = data[0] << 8 | data[1]

    bus.write_byte_data(MPU6050, ACCEL_ZOUT_H, 0)
    data = bus.read_i2c_block_data(MPU6050, ACCEL_ZOUT_H, 2)
    AcZ = data[0] << 8 | data[1]

    bus.write_byte_data(MPU6050, GYRO_XOUT_H, 0)
    data = bus.read_i2c_block_data(MPU6050, GYRO_XOUT_H, 2)
    GyX = data[0] << 8 | data[1]

    AcYc = AcY - self_balancing_bike.offsets.AcY
    AcZc = AcZ - self_balancing_bike.offsets.AcZ
    GyX -= self_balancing_bike.GyX_offset

    robot_angle += GyX * self_balancing_bike.LOOP_TIME / 1000 / 65.536
    Acc_angle = -math.atan2(AcYc, -AcZc) * 57.2958
    robot_angle = robot_angle * self_balancing_bike.GYRO_AMOUNT + Acc_angle * (1.0 - self_balancing_bike.GYRO_AMOUNT)

    if abs(robot_angle) > 10:
        vertical = False
    if abs(robot_angle) < 0.4:
        vertical = True

def angle_setup():
    bus.write_byte_data(MPU6050, PWR_MGMT_1, 0)
    bus.write_byte_data(MPU6050, ACCEL_CONFIG, accSens << 3)
    bus.write_byte_data(MPU6050, GYRO_CONFIG, gyroSens << 3)

    for i in range(1024):
        angle_calc()
        GyX_offset_sum += self_balancing_bike.GyX
        time.sleep(0.003)

    GyX_offset = GyX_offset_sum >> 10
    beep()
    beep()
    print("GyX offset:", GyX_offset)

def battVoltage(voltage):
    if voltage > 8 and voltage <= 9.5:
        self_balancing_bike.GPIO.output(self_balancing_bike.BUZZER, self_balancing_bike.GPIO.HIGH)
    else:
        self_balancing_bike.GPIO.output(self_balancing_bike.BUZZER, self_balancing_bike.GPIO.LOW)

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