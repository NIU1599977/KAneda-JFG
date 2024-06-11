import math
class Remrc:
  def __init__(self, my_mpu):
        self.my_mpu = my_mpu # Note that the MPU return data in [m/s**2] for accelerometer and [deg/s] for gyro
        self.K1 = 115
        self.K2 = 15.00
        self.K3 = 8.00
        self.K4 = 0.60
        self.alpha = 0.4
        self.gyro_amount = 0.996
        self.loop_time = 10
        self.vertical = False

  #void angle_calc() {
  def get_angle(self):

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

    #robot_angle += GyX * loop_time / 1000 / 65.536;
    robot_angle += GyX * self.loop_time / 1000 / 65.536     

    #Acc_angle = -atan2(AcYc, -AcZc) * 57.2958;        
    Acc_angle = -math.atan2(AcYc, -AcZc) * 57.2958

    #robot_angle = robot_angle * Gyro_amount + Acc_angle * (1.0 - Gyro_amount);
    robot_angle = robot_angle * self.gyro_amount + Acc_angle * (1.0 - self.gyro_amount)
    
    if (abs(robot_angle) > 10): self.vertical = False
    if (abs(robot_angle) < 0.4): self.vertical = True

    return robot_angle, GyX

  # def angle_calc(self):
  #   acc_data = imu.get_data()
  #   # Revisar por posibles offsets o usar valores raw (ej. gyro_x)
  #   self.angle += acc_data["Gx"] * LOOP_TIME / 1000 / 65.536
  #   self.acc_angle = -math.atan2(acc_data["Ay"], -acc_data["Az"]) * 57.2958
  #   self.angle = self.angle * self.GYRO_AMOUNT + self.acc_angle * (1.0 - self.GYRO_AMOUNT)

  #   if abs(self.angle) > 10:
  #     self.vertical = False
  #   if abs(self.angle) < 0.4:
  #     self.vertical = True

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

  # def angle_setup(self):
  #   for i in range(1024): # 1024 ?
  #     self.angle_calc()
  #     time.sleep(0.003)

