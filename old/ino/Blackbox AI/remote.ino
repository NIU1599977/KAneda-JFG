/*
  STX y ETX son constantes que representan el inicio y el fin de la transmisión, respectivamente.
  cmd es un array que almacena los comandos recibidos.
  buttonStatus es una variable que almacena el estado de los botones.
*/
#define    STX          0x02
#define    ETX          0x03
byte cmd[8] = {0, 0, 0, 0, 0, 0, 0, 0};
byte buttonStatus = 0; 

/*
  Esta función lee los parámetros de control enviados desde un smartphone.
  Si hay datos disponibles en el puerto serie, se leen y se almacenan en cmd.
  Si el primer byte es STX, se leen los siguientes bytes.
  Si se recibe ETX y el número de bytes es 2 o 7, se interpretan como datos de botón o joystick, respectivamente.
*/
void readControlParameters() {
  if (Serial.available())  {                           // data received from smartphone
    //delay(1);
    cmd[0] =  Serial.read();  
    if(cmd[0] == STX)  {
      int i = 1;      
      while (Serial.available())  {
        //delay(1);
        cmd[i] = Serial.read();
        if(cmd[i] > 127 || i > 7)                 break;     // Communication error
        if((cmd[i] == ETX) && (i == 2 || i == 7)) break;     // Button or Joystick data
        i++;
      }
      if (i == 2) getButtonState(cmd[1]);                  // 3 Bytes  ex: < STX "C" ETX >
      else if (i == 7) getJoystickState(cmd);              // 6 Bytes  ex: < STX "200" "180" ETX >
    }
  } 
}
/*
  Esta función interpreta los datos del joystick.
  Convierte los bytes de los datos en valores enteros.
  Aplica un offset para evitar la transmisión de números negativos.
  Si los valores están fuera del rango permitido, se descartan.
  Si los valores están dentro de la “zona muerta”, se ignoran.
  Los valores se mapean a las velocidades y direcciones máximas permitidas.
*/
void getJoystickState (byte data[8])    {
  int joyX = (data[1] - 48) * 100 + (data[2] - 48) * 10 + (data[3] - 48);   // obtain the Int from the ASCII representation
  int joyY = (data[4] - 48) * 100 + (data[5] - 48) * 10 + (data[6] - 48);
  joyX = joyX - 200;                                                        // Offset to avoid
  joyY = joyY - 200;                                                        // transmitting negative numbers

  if (joyX < -100 || joyX > 100 || joyY < -100 || joyY > 100) return;       // commmunication error
  if (joyX < - 10 || joyX > 10)  { // dead zone
    if (joyX > 0) // exponential
      steering_remote = (-joyX * joyX + 0.1 * joyX) / 100.0;
    else   
      steering_remote = (joyX * joyX + 0.1 * joyX) / 100.0;
  } else 
      steering_remote = 0;
  steering_remote = -map(steering_remote, -100, 100, -STEERING_MAX, STEERING_MAX);
  if (joyY < - 10 || joyY > 10)  // dead zone 
     speed_remote = map(joyY, 100, -100, SPEED_MAX, -SPEED_MAX);
  else
     speed_remote = 0;        
}

/*
  Esta función interpreta el estado de los botones.
  Según el estado recibido, se actualiza la variable buttonStatus.
*/
void getButtonState (int bStatus)  {
  switch (bStatus) {
// -----------------  BUTTON #1  -----------------------
   case 'A':
      buttonStatus |= B000001;        // ON
      break;
    case 'B':
      buttonStatus &= B111110;        // OFF
      break;
// -----------------  BUTTON #2  -----------------------
   case 'C':
      buttonStatus |= B000010;        // ON    
      break;
    case 'D':
      buttonStatus &= B111101;        // OFF    
      break;
  }
}
/*
  Esta función convierte el estado de los botones en una cadena de texto.
*/
String getButtonStatusString()  {
  String bStatus = "";
  for (int i = 0; i < 6; i++)  {
    if (buttonStatus & (B100000 >> i))      bStatus += "1";
    else                                    bStatus += "0";
  }
  return bStatus;
}
/*
  Esta función envía los parámetros de control a través del puerto serie.
  Envía el estado de los botones y otros campos de datos.
*/
void sendControlParameters() {
  Serial.print((char)STX);                                                // Start of Transmission
  Serial.print(getButtonStatusString());  Serial.print((char)0x1);        // buttons status feedback
  Serial.print(0);                        Serial.print((char)0x4);        // datafield #1
  Serial.print(0);                        Serial.print((char)0x5);        // datafield #2
  Serial.print(0);                                                        // datafield #3
  Serial.print((char)ETX);                                                // End of Transmission
}