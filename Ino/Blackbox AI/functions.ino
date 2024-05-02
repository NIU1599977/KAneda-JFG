#define MPU6050 0x68              // Define la dirección del dispositivo MPU6050 en el bus I2C.

//Son las direcciones de los registros de configuración del acelerómetro y del giroscopio, respectivamente.
#define ACCEL_CONFIG 0x1C         // Accelerometer configuration address
#define GYRO_CONFIG  0x1B         // Gyro configuration address

// Registers: Accelerometer, Temp, Gyroscope
// Las constantes ACCEL_XOUT_H, ACCEL_XOUT_L, ACCEL_YOUT_H, etc., son las direcciones de los registros 
// donde el MPU6050 almacena los datos del acelerómetro, la temperatura y el giroscopio.
#define ACCEL_XOUT_H 0x3B
#define ACCEL_XOUT_L 0x3C
#define ACCEL_YOUT_H 0x3D
#define ACCEL_YOUT_L 0x3E
#define ACCEL_ZOUT_H 0x3F
#define ACCEL_ZOUT_L 0x40
#define TEMP_OUT_H 0x41
#define TEMP_OUT_L 0x42
#define GYRO_XOUT_H 0x43
#define GYRO_XOUT_L 0x44
#define GYRO_YOUT_H 0x45
#define GYRO_YOUT_L 0x46
#define GYRO_ZOUT_H 0x47
#define GYRO_ZOUT_L 0x48

// Son las direcciones de los registros de gestión de energía del MPU6050. 
// Se utilizan para despertar el dispositivo o ponerlo en modo de bajo consumo.
#define PWR_MGMT_1 0x6B
#define PWR_MGMT_2 0x6C

//  Estas líneas definen la sensibilidad del acelerómetro y del giroscopio. 
// Los comentarios indican los rangos de medición correspondientes a cada valor.
#define accSens 0             // 0 = 2g, 1 = 4g, 2 = 8g, 3 = 16g
#define gyroSens 1            // 0 = 250rad/s, 1 = 500rad/s, 2 1000rad/s, 3 = 2000rad/s

/*
Esta función escribe un valor en una dirección específica de un dispositivo. 
Utiliza la biblioteca Wire para la comunicación I2C. Wire.beginTransmission(device) inicia la transmisión al dispositivo,
Wire.write(address) y Wire.write(value) escriben la dirección y el valor, y Wire.endTransmission(true) termina la transmisión.
*/
void writeTo(byte device, byte address, byte value) {
  Wire.beginTransmission(device);
  Wire.write(address);
  Wire.write(value);
  Wire.endTransmission(true);
}

/*
  Esta función guarda los valores de calibración en la memoria EEPROM del Arduino. EEPROM.put(0, offsets) guarda los valores de calibración en la dirección 0 de la EEPROM. Luego, después de un breve retraso, EEPROM.get(0, offsets) recupera los valores de calibración para verificar que se hayan guardado correctamente. Si el ID de los valores de calibración es 35, entonces se considera que el dispositivo está calibrado y se desactiva el modo de calibración. 
  Finalmente, se imprime un mensaje en el monitor serial y se emite un pitido para indicar que la calibración se ha completado.
*/
void save() {
    EEPROM.put(0, offsets);
    delay(100);
    EEPROM.get(0, offsets);
    if (offsets.ID == 35) calibrated = true;
    calibrating = false;
    Serial.println("calibrating off");
    beep();
}

/*
  Esta función hace que el zumbador (BUZZER) emita un pitido. digitalWrite(BUZZER, HIGH) enciende el zumbador, delay(70) lo mantiene encendido durante 70 milisegundos, 
  digitalWrite(BUZZER, LOW) lo apaga, y delay(80) espera 80 milisegundos antes de continuar.
*/
void beep() {
    digitalWrite(BUZZER, HIGH);
    delay(70);
    digitalWrite(BUZZER, LOW);
    delay(80);
}

/*
  Esta función calcula el ángulo del robot utilizando los datos del acelerómetro y del giroscopio. Primero, lee los datos del acelerómetro y del giroscopio del MPU6050. Luego, calcula el ángulo del robot utilizando una combinación de los datos del acelerómetro (ángulo de inclinación) y del giroscopio (velocidad angular). 
  Finalmente, verifica si el robot está en posición vertical.
*/
void angle_calc() {

  Wire.beginTransmission(MPU6050);
  Wire.write(ACCEL_YOUT_H);                       
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6050, 2, true);   
  AcY = Wire.read() << 8 | Wire.read(); 
  
  Wire.beginTransmission(MPU6050);
  Wire.write(ACCEL_ZOUT_H);                  
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6050, 2, true);  
  AcZ = Wire.read() << 8 | Wire.read(); 

  Wire.beginTransmission(MPU6050);
  Wire.write(GYRO_XOUT_H);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6050, 2, true); 
  GyX = Wire.read() << 8 | Wire.read();

  AcYc = AcY - offsets.AcY;
  AcZc = AcZ - offsets.AcZ;
  GyX -= GyX_offset;

  robot_angle += GyX * loop_time / 1000 / 65.536;                 
  Acc_angle = -atan2(AcYc, -AcZc) * 57.2958;   
  robot_angle = robot_angle * Gyro_amount + Acc_angle * (1.0 - Gyro_amount);
  
  if (abs(robot_angle) > 10) vertical = false;
  if (abs(robot_angle) < 0.4) vertical = true;
  
}

/*
  Esta función inicializa el MPU6050 y calcula el desplazamiento del giroscopio. 
  El desplazamiento del giroscopio es la lectura del giroscopio cuando el robot está en reposo, y se utiliza para calibrar el giroscopio.
*/
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

/*
  Esta función verifica el voltaje de la batería y activa un zumbador si el voltaje está entre 8 y 9.5 voltios.
*/
void battVoltage(double voltage) {
  if (voltage > 8 && voltage <= 9.5) {
    digitalWrite(BUZZER, HIGH);
  } else {
    digitalWrite(BUZZER, LOW);
  }
}
/*
  Motor1 y Motor2
  Estas funciones controlan la velocidad y la dirección de los motores. Si sp es positivo, el motor se mueve en una dirección, y si es negativo, se mueve en la dirección opuesta.
*/
void Motor1_control(int sp) {
  if (sp > 0) digitalWrite(DIR_1, LOW);
    else digitalWrite(DIR_1, HIGH);
  analogWrite(PWM_1, 255 - abs(sp));
}

void Motor2_control(int sp) {
  if (sp > 0) digitalWrite(DIR_2, LOW);
    else digitalWrite(DIR_2, HIGH);
  analogWrite(PWM_2, 255 - abs(sp));
}
/*
  Esta función permite ajustar los parámetros de control del robot a través del puerto serie. 
  Puedes aumentar o disminuir los valores de los parámetros de control enviando comandos específicos.
*/
int Tuning() {
  if (!Serial.available())  return 0;
  delay(2);
  char param = Serial.read();               // get parameter byte
  if (!Serial.available()) return 0;
  char cmd = Serial.read();                 // get command byte
  Serial.flush();
  switch (param) {
    case 'p':
      if (cmd == '+')    K1 += 1;
      if (cmd == '-')    K1 -= 1;
      printValues();
      break;
    case 'i':
      if (cmd == '+')    K2 += 0.5;
      if (cmd == '-')    K2 -= 0.5;
      printValues();
      break;
    case 's':
      if (cmd == '+')    K3 += 0.2;
      if (cmd == '-')    K3 -= 0.2;
      printValues();
      break;  
    case 'a':
      if (cmd == '+')    K4 += 0.05;
      if (cmd == '-')    K4 -= 0.05;
      printValues();
      break;    
    case 'c':
      if (cmd == '+' && !calibrating) {
        calibrating = true;
        Serial.println("calibrating on");
      }
      if (cmd == '-' && calibrating)  {
          offsets.ID = 35;
          offsets.AcZ = AcZ + 16384;
          offsets.AcY = AcY;
          Serial.print("AcY: "); Serial.print(offsets.AcY); Serial.print(" AcZ: "); Serial.println(offsets.AcZ); 
          save();
      }
      break;                
   }
   return 1;
}

/*Esta función imprime los valores de los parámetros de control en el puerto serie.*/
void printValues() {
  Serial.print(" K1: "); Serial.print(K1);
  Serial.print(" K2: "); Serial.print(K2);
  Serial.print(" K3: "); Serial.print(K3,4);
  Serial.print(" K4: "); Serial.println(K4,4);
}

/*Esta función lee los valores de los encoders de los motores. Los encoders se utilizan para medir la velocidad y la posición de los motores.*/
void ENC_READ() {
  byte cur = (!digitalRead(ENC_1) << 1) + !digitalRead(ENC_2);
  byte old = pos & B00000011;
  byte dir = (pos & B00110000) >> 4;
 
  if (cur == 3) cur = 2;
  else if (cur == 2) cur = 3;
 
  if (cur != old) {
  if (dir == 0) {
    if (cur == 1 || cur == 3) dir = cur;
    } else {
      if (cur == 0) {
        if (dir == 1 && old == 3) enc_count--;
        else if (dir == 3 && old == 1) enc_count++;
        dir = 0;
      }
    }
    pos = (dir << 4) + (old << 2) + cur;
  }
}
