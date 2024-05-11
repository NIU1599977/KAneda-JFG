import serial
import self_balancing_bike
import time

# Definir constantes para la velocidad y el tiempo de giro
MAX_SPEED_TIME = 0.00059 
SPEED = 10  # Ajustar según sea necesario
TURN_TIME = 0.01  # Ajustar según sea necesario

def move(distance, angle):
    # Calcular el tiempo necesario para moverse la distancia deseada
    move_time = abs(distance / SPEED)
    
    # Mover la bicicleta
    if distance > 0:
        self_balancing_bike.speed_remote = self_balancing_bike.SPEED_MAX
    else:
        self_balancing_bike.speed_remote = -self_balancing_bike.SPEED_MAX
    time.sleep(move_time)
    self_balancing_bike.speed_remote = 0  # Detener la bicicleta
    
    # Calcular el tiempo necesario para girar el ángulo deseado
    turn_time = abs(angle * TURN_TIME)
    
    # Girar la bicicleta
    if angle > 0:
        self_balancing_bike.steering_remote = self_balancing_bike.STEERING_MAX
    else:
        self_balancing_bike.steering_remote = -self_balancing_bike.STEERING_MAX
    time.sleep(turn_time)
    self_balancing_bike.steering_remote = 0  # Detener el giro

# Ejemplo de uso: avanza 30 cm recto, luego gira 90 grados y luego avanza recto 50 cm
#move(30, 0)
#move(0, 90)
#move(50, 0)
