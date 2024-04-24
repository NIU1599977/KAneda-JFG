import serial
import self_balancing_bike
# Configuración del puerto serie
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)  # Puerto serie en Raspberry Pi Zero y velocidad de 115200 baudios

STX = 0x02
ETX = 0x03
cmd = [0,0,0,0,0,0,0,0]
buttonStatus = 0

def readControlParameters():
  if(ser.available()):
    cmd[0] = ser.read()
    if(cmd[0] == STX):
      i = 1
      while(ser.available()):
        cmd[i] = ser.read()
        if(cmd[i] > 127 or i > 7):
          break
        if((cmd[i] == ETX) and (i == 2 or i == 7)):
          break
        i = i + 1
      if(i == 2):
         getButtonState(cmd[1])
      elif (i == 7):
         getJoystickState(cmd)


def getJoystickState(data):
    joyX = (int(chr(data[1])) - 48) * 100 + (int(chr(data[2])) - 48) * 10 + (int(chr(data[3])) - 48)  # Obtiene el entero a partir de la representación ASCII
    joyY = (int(chr(data[4])) - 48) * 100 + (int(chr(data[5])) - 48) * 10 + (int(chr(data[6])) - 48)
    joyX -= 200  # Desplazamiento para evitar transmitir números negativos
    joyY -= 200

    if joyX < -100 or joyX > 100 or joyY < -100 or joyY > 100:
        return  # Error de comunicación

    if -10 < joyX < 10:  # Zona muerta
        steering_remote = 0
    else:
        if joyX > 0:
            steering_remote = (-joyX * joyX + 0.1 * joyX) / 100.0  # Exponencial
        else:
            steering_remote = (joyX * joyX + 0.1 * joyX) / 100.0
    steering_remote = -map(steering_remote, -100, 100, -self_balancing_bike.STEERING_MAX, self_balancing_bike.STEERING_MAX)

    if -10 < joyY < 10:  # Zona muerta
        speed_remote = 0
    else:
        speed_remote = map(joyY, 100, -100, self_balancing_bike.SPEED_MAX, -self_balancing_bike.SPEED_MAX)


def getButtonState(bStatus):
    if bStatus == 'A':
        buttonStatus |= 0b000001  # Enciende el botón #1
    elif bStatus == 'B':
        buttonStatus &= 0b111110  # Apaga el botón #1
    elif bStatus == 'C':
        buttonStatus |= 0b000010  # Enciende el botón #2
    elif bStatus == 'D':
        buttonStatus &= 0b111101  # Apaga el botón #2


def getButtonStatusString():
    bStatus = ""
    for i in range(6):
        if buttonStatus & (0b100000 >> i):
            bStatus += "1"
        else:
            bStatus += "0"
    return bStatus

def sendControlParameters():
    transmission = chr(STX)  # Start of Transmission
    transmission += getButtonStatusString()
    transmission += chr(0x1)  # Buttons status feedback
    transmission += chr(0) + chr(0x4)  # Datafield #1
    transmission += chr(0) + chr(0x5)  # Datafield #2
    transmission += chr(0)  # Datafield #3
    transmission += chr(ETX)  # End of Transmission
    
    # Envía la transmisión por el puerto serie
    ser.write(transmission.encode())  # ser es tu objeto de comunicación serie
