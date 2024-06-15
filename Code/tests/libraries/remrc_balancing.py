import math
import time
import numpy as np

class Remrc:
  def __init__(self, my_mpu):
        self.my_mpu = my_mpu # Note that the MPU return data in [m/s**2] for accelerometer and [deg/s] for gyro
        self.K1 = 115
        self.K2 = 15.00
        self.K3 = 8.00
        self.K4 = 0.60
        self.alpha = 0.4
        self.gyro_amount = 0.996
        self.GyX_offset = 0
        self.robot_angle = 0
        self.gyroXfilt = 0
        

  #void angle_calc() {
  def get_angle(self,dt):

    # Wire.beginTransmission(MPU6050);
    # Wire.write(ACCEL_YOUT_H);                       
    # Wire.endTransmission(false);
    # Wire.requestFrom(MPU6050, 2, true);   
    # AcY = Wire.read() << 8 | Wire.read();
    AcYc = self.my_mpu.get_accel_data()['y']
    
    # Wire.beginTransmission(MPU6050);
    # Wire.write(ACCEL_ZOUT_H);                  
    # Wire.endTransmission(false);
    # Wire.requestFrom(MPU6050, 2, true);  
    # AcZ = Wire.read() << 8 | Wire.read(); 
    AcZc = self.my_mpu.get_accel_data()['z']

    # Wire.beginTransmission(MPU6050);
    # Wire.write(GYRO_XOUT_H);
    # Wire.endTransmission(false);
    # Wire.requestFrom(MPU6050, 2, true); 
    # GyX = Wire.read() << 8 | Wire.read();
    GyX = self.my_mpu.get_gyro_data()['x']
    GyX -= self.GyX_offset

    #robot_angle += GyX * loop_time / 1000 / 65.536;
    self.robot_angle = GyX * dt / 1000 / 65.536     

    #Acc_angle = -atan2(AcYc, -AcZc) * 57.2958;        
    Acc_angle = -math.atan2(-AcYc, AcZc) * 57.2958

    #robot_angle = robot_angle * Gyro_amount + Acc_angle * (1.0 - Gyro_amount);
    self.robot_angle = self.robot_angle * self.gyro_amount + Acc_angle * (1.0 - self.gyro_amount)
    # print("angle: ", self.robot_angle)
    if (abs(self.robot_angle) > 10): 
        bb = 0
    else: #if (abs(self.robot_angle) < 0.4): 
        # gyroXfilt = alpha * gyroX + (1 - alpha) * gyroXfilt;
        self.gyroXfilt = self.alpha * GyX + (1 - self.alpha) * self.gyroXfilt
        # int pwm = constrain(K1 * robot_angle + K2 * gyroXfilt + K3 * motor_speed + K4 * motor_pos, -255, 255); 
        bb = abs(self.K1 * self.robot_angle + self.K2 * self.gyroXfilt / 10) #  + filter.K3 * motor_speed -> en teoria esto es lo rapido que va la moto
        bb = max(0, min(bb, 40))
    # print("Angulo [deg] = ", int(self.robot_angle)," Velocidad angular [deg/s] = ", int(bb))

    return self.robot_angle, GyX, bb

  """
  void angle_setup() {
    Wire.begin();
    delay(100);
    writeTo(MPU6050, PWR_MGMT_1, 0);
    writeTo(MPU6050, ACCEL_CONFIG, accSens << 3);   // Specifying output scaling of accelerometer
    writeTo(MPU6050, GYRO_CONFIG, gyroSens << 3);   // Specifying output scaling of gyroscope
    delay(100);

    for (int i = 0; i < 1024; i++) {
      angle_calc();
      GyX_offset_sum += GyX;
      delay(3);
    }
    GyX_offset = GyX_offset_sum >> 10;
    beep();
    beep();
    Serial.print("GyX offset: ");  Serial.println(GyX_offset);
  }
  """

  def angle_setup(self):
    GyX_offset_sum = 0
    time.sleep(0.1)
    for i in range(1024): # 1024 ?
      _, GyX, _ = self.get_angle(0)
      GyX_offset_sum += GyX
      time.sleep(0.003)
    self.GyX_offset = GyX_offset_sum // 1024
    print("GyX offset: ", self.GyX_offset)

  def calibrate(self): # Adaptación de Tuning() (functions.ino)
    calibrated = False
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