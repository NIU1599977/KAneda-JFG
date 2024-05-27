# KAneda-JFG

Motocicleta auto-balanceable capaz de reconocer señales de tráfico mediante visión por computador.

## Tabla de Contenidos

+ [Descripción del Proyecto](#descripción-del-proyecto)
+ [Componentes Electrónicos](#componentes-electrónicos)
+ [Componentes Mecánicos](#componentes-mecánicos)
+ [Esquema Eléctrico](#esquema-eléctrico)
+ [Diseño 3D](#diseño-3d)
+ [Arquitectura del Software](#arquitectura-del-software)
+ [Algorítmica](#algorítmica)
+ [Visión por Computador](#visión-por-computador)
+ [Simulación](#simulación)
+ [Contribuciones y Agradecimientos](#contribuciones-y-agradecimientos)
+ [Autoría](#autoría)
+ [Bibliografía](#bibliografía)

## Descripción del Proyecto

Este proyecto de motocicleta auto-balanceable surge con la visión de desarrollar un vehículo autónomo capaz de detectar y obedecer las señales de tráfico sin la intervención de un conductor. El propósito principal es brindar a la Dirección General de Tráfico (DGT) una herramienta para llevar a cabo demostraciones y programas educativos sobre seguridad vial. Utilizando técnicas avanzadas de visión por computador, nuestra moto puede interpretar y responder de manera precisa a las señales del entorno, lo que la convierte en un prototipo innovador en el campo de la movilidad autónoma.

La tecnología de auto-balanceo de la motocicleta se basa en el proyecto [Self-Balancing-Bike](https://github.com/remrc/Self-Balancing-Bike), realizado por [remrc](https://github.com/remrc) en Arduino.

## Componentes Electrónicos

| Componente | Imagen | Componente | Imagen |
| --- | --- | --- | --- |
| [Kit Raspberry Pi Zero W + MicroSD 32GB](https://tienda.bricogeek.com/placas-raspberry-pi/1082-kit-basico-raspberry-pi-zero-wifi-microsd-32gb.html) | <img src="https://tienda.bricogeek.com/4669-thickbox_default/kit-basico-raspberry-pi-zero-wifi-microsd-32gb.jpg" width="200" height="150"/> | [Cámara Raspberry Pi v2 - 8 Megapíxeles](https://tienda.bricogeek.com/accesorios-raspberry-pi/822-camara-raspberry-pi-v2-8-megapixels.html) | <img src="https://tienda.bricogeek.com/3115-thickbox_default/camara-raspberry-pi-v2-8-megapixels.jpg" width="200" height="150"/> |
| [Cable cámara Raspberry Pi Zero (30cm)](https://tienda.bricogeek.com/accesorios-raspberry-pi/1562-cable-camara-raspberry-pi-zero-30cm.html) | <img src="https://tienda.bricogeek.com/7022-thickbox_default/cable-camara-raspberry-pi-zero-30cm.jpg" width="200" height="150"/> | [Módulo GY-521 Acelerómetro y Giroscopio MPU-6050](https://tienda.bricogeek.com/acelerometros/1682-modulo-gy-521-acelerometro-y-giroscopio-mpu-6050.html) | <img src="https://tienda.bricogeek.com/7776-thickbox_default/modulo-gy-521-acelerometro-y-giroscopio-mpu-6050.jpg" width="200" height="150"/> |
| [Micro servo miniatura SG90](https://tienda.bricogeek.com/servomotores/968-micro-servo-miniatura-sg90.html) | <img src="https://tienda.bricogeek.com/3972-thickbox_default/micro-servo-miniatura-sg90.jpg" width="200" height="150"/> | [Motor paso a paso 28BYJ-48 (5V) con driver ULN2003](https://tienda.bricogeek.com/motores-paso-a-paso/969-motor-paso-a-paso-28byj-48-5v-con-driver-uln2003.html) | <img src="https://tienda.bricogeek.com/5892-thickbox_default/motor-paso-a-paso-28byj-48-5v-con-driver-uln2003.jpg" width="200" height="150"/> |
| [Motor Micro Metal LP con reductora 10:1](https://tienda.bricogeek.com/motores/113-motor-micro-metal-lp-con-reductora-10-1.html) | <img src="https://tienda.bricogeek.com/288-thickbox_default/motor-micro-metal-lp-con-reductora-10-1.jpg" width="200" height="150"/> | [Controlador de motores TB6612FNG](https://tienda.bricogeek.com/controladores-motores/999-controlador-de-motores-tb6612fng.html) | <img src="https://tienda.bricogeek.com/4166-large_default/controlador-de-motores-tb6612fng.jpg" width="200" height="150"/> |
| [Bateria Lipo 1000mAh / 3.7V - 603050](https://tienda.bricogeek.com/baterias-lipo/135-bateria-lipo-1000mah-603050-37v.html) | <img src="https://tienda.bricogeek.com/385-thickbox_default/bateria-lipo-1000mah-603050-37v.jpg" width="200" height="150"/> | [Cargador LiPo PowerBoost 500](https://tienda.bricogeek.com/convertidores-de-voltaje/677-cargador-lipo-powerboost-500.html) | <img src="https://tienda.bricogeek.com/2303-thickbox_default/cargador-lipo-powerboost-500.jpg" width="200" height="150"/> |

## Componentes Mecánicos

### Movimiento

| Componente | Imagen | Unidades |
| --- | --- | --- |
| [Rueda Solarbotics antideslizante](https://tienda.bricogeek.com/robotica/230-rueda-solarbotics-antideslizante.html) | <img src="https://tienda.bricogeek.com/3429-thickbox_default/rueda-solarbotics-antideslizante.jpg" width="200" height="150"/> | 2 |
| [Rodamiento 608-2RS (8x22x7mm)](https://tienda.bricogeek.com/rodamientos/1294-rodamiento-608-2rs-8x22x7mm.html) | <img src="https://tienda.bricogeek.com/9166-thickbox_default/rodamiento-608-2rs-8x22x7mm.jpg" width="200" height="150"/> | 2 |

### Tornillos

| Métrica | Longitud (cm) | Partes | Unidades | Tuercas |
| --- | --- | --- | --- | --- |
| M1 | 1 | Soporte Motor - Motor | 2 | Sí |
| M2 | 1 | Cámara | 2 | Sí |
| M2 | 2 | Servo | 2 | Sí |
| M3 | 1 | Soporte Stepper | 2 | Sí |
| M3 | 1,5 | Manillar, Frontal - Base, Base - Motor, Soporte Motor - Soporte Motor, Soporte Motor - Soporte Motor, Soporte Motor - Base | 12 | Sí |
| M3 | 2 | Culo | 4 | Sí |
| M3 | 3 | Base - Base | 2 | Sí |
| M4 | 0,5 | Volante de Inercia | 16 | Sí |

## Esquema Eléctrico

![KAneda-JFG](fritzing/KAneda-JFG.jpg)

## Diseño 3D

Para el diseño 3D se ha optado por emplear los softwares FreeCAD y Cinema4D debido a que uno de los integrantes ya estaba familiarizado con él. El esqueleto de la motocicleta ha venido dado por el proyecto realizado por remrc, el cual tiene compartido en la página Thingiverse los [modelos](https://www.thingiverse.com/thing:5887157/files) que ha utilizado.

Estos modelos se han modificado para adecuarlos a nuestros componentes y de esta manera no exceder el presupuesto proporcionado por el profesorado. Los modelos han sido modificados de la siguiente manera.

### Manillar

Para el manillar, se ha utilizado el micro-servo SG90, por ello, ha sido necesario adaptar la pieza donde se asienta este componente.

| Antes | Después |
| --- | --- |
| ![1715457172442](image/README/1715457172442.png) | ![1715457205373](image/README/1715457205373.png) |

### Volante de inercia

El volante de inercia es el alma de esta motocicleta, por tanto su diseño se ha intentado mantener con respecto al utilizado por remrc. En nuestro caso, hemos adaptado el eje de adhesión para asegurar la compatibilidad con nuestro motor pololu.

| Antes | Después |
| --- | --- |
| ![1715457312993](image/README/1715457312993.png) | ![1715457302456](image/README/1715457302456.png) |

### Cámara RPi

La motocicleta tiene soporte para utilizar visión por computador, por ello, se ha modificado la pieza que une al manillar con el cuerpo central de la motocicleta. La cámara se situaría en un lateral, esto es debido a que si se situase al frente del vehiculo, el cable no sería suficiente para llegar hasta el cuerpo central. La visión se vería ligeramente mermada a un lado por el propio manillar y la rueda delantera pero no debería suponer ningún problema.

| Antes | Después |
| --- | --- |
| ![1715457103599](image/README/1715457103599.png) | ![1715457078462](image/README/1715457078462.png) |


| Visión de la cámara |
| --- |
| ![camera_vision](image/README/vision_camara.png) |

### Parte posterior

La parte posterior de la motocicleta ha sido completamente rediseñada desde cero debido al límite presupuestario. En un principio remrc utilizaba un stepper y una correa para transmitir la potencia a la rueda trasera, nosotros hemos optado por utilizar un micro-stepper y transmitir la potencia mediante el uso de dos engranajes de 16 dientes, disponibles en [thingiverse](https://www.thingiverse.com/thing:146289). Además, hemos optado por añadir un rodamiento de 22mm x 8mm para mitigar las imprecisiones que puedan surgir utilizando un eje transversal e impresión 3D. Con ello, nuestra parte trasera quedaría tal que así.

| Antes | Después |
| --- | --- |
| ![1715457360946](image/README/1715457360946.png) | ![1715457400725](image/README/1715457400725.png) |

## Arquitectura del Software

En relación con el componente de software de nuestro proyecto, hemos emprendido la tarea de traducir e interpretar el código del proyecto de referencia, que originalmente fue diseñado para Arduino (código **.ino**). Sin embargo, la principal complejidad de nuestro robot radica en que no estamos utilizando Arduino, sino una Raspberry Pi Zero. Como resultado, hemos tenido que investigar exhaustivamente sobre las librerías adecuadas para nuestra placa y además adaptar su código y reestructurarlo (e incluso añadir funcionalidades) en base a nuestro proyecto.

El software de Kaneda-JFG se compone de cuatro módulos, los cuales, en su totalidad, habilitarán la funcionalidad completa del robot.


### Módulo de Detección de señales
Este módulo, tal y como indica su nombre se centra en la detección de la señales de tráfico y la reacción del robot a cada una de estas. 

### Módulo de control de la inclinación
El módulo de control de inclinación de la moto se ejecuta mediante un bucle que constantemente utiliza el **Filtro de Kalman** para predecir en aproximadamente 1 segundo, la inclinación que tendrá la moto.

De esta forma, al conocer la próxima inclinación del robot se podrá contrarrestar utilizando el volante de inercia para mantener la moto en pie en todo momento.

### Módulo de control de la moto
Otro módulo importante de la moto, es el módulo que nos permite controlar la moto. A la vez que este va prediciendo su inclinación con el filtro de kalman (módulo de control de la inclinación) también espera comandos que el usuario debe introducir.

El usuario debe introducir una serie de comandos para indicar el camino que debe recorrer la moto, indicando en todo momento la distancia a recorrer y el ángulo (si tiene que ir recto o girar).

**Ejemplo:**
>> 20,0 0,90 5,0 0,45 35,0 0,0 (ve recto 20cm, gira 90º derecha, ve recto 5cm, gira 45º derecha, ve recto 35cm y para).


### Módulo de Interacción HW/SW
Este es de los módulos más importante del programa que controla la moto, ya que es el que permite la comunicación entre la parte física de la moto con la parte Software de esta.

Junta cada una de las funcionalidades que ofrece la moto y las coordina según los datos que envíen los sensores de la moto, los comandos introducidos por el usuario, etc.

## Algorítmica

### Filtro de Kalman

Para poder controlar la orientación de la moto y evitar que se caiga, hemos pensado en implementar el famoso algoritmo conocido como **Filtro de Kalman**.

#### Breve descripción del filtro de Kalman

El filtro de Kalman se trata de un algoritmo que puede estimar parámetros observables y no observables con gran precisión en tiempo real. Es utilizado para estimar las variables de un sistema basándose en medidas con ruido, calcula las diferentes probabilidades del estado de un sistema. Lo podemos ver como una caja negra, donde las entradas son ruidosas y, a veces, contienen mediciones inexactas. Y los resultados son menos ruidosos y tienen más precisión.

Este algoritmo es muy utilizado en robótica y sistemas en tiempo real que necesitan información confiable. Su importancia recae en poder estimar parámetros del sistema que no se pueden medir u observar con precisión, permitiendo así a los sistemas tener un mayor control y, por tanto, más capacidades.

Este algoritmo se basa principalmente en 2 pasos:

1) **Predicción:** Donde, basándose en el estado anterior del sistema se predice el estado actual del sistema y su incertidumbre.
2) **Actualización (o Corrección):** Se utilizan las mediciones actuales para actualizar la estimación del estado y reducir la incertidumbre (el ruido). 

Estos 2 pasos se repiten en cada paso de tiempo para producir una estimación del estado de forma más precisa.

#### ¿Cómo encaja con nuestro proyecto?

Precisamente, por lo explicado en el subapartado anterior, el filtro de Kalman se trata de una herramienta poderosa que nos permitirá obtener la futura inclinación que tomará la moto antes de que ocurra.
De esta manera, sabiendo este dato, nos permitirá corregir la inclinación de la moto ajustando los parámetros del volante de inercia (ajustando potencia y dirección) según la inclinación de la moto.


## Visión por Computador
### Breve descripción de la idea de visión por computador
La implementación que queremos hacer, va sobre poner una camará en la moto, para que cuando vea una señal, poder reaccionar a ella dependiendo del significado de la señal.
### YOLO
Yolo es la tecnologia que usaremos para nuestra implementación para el tema de la visión por computador. Yolo se refiere a "You Only Look Once", un algoritmo de detección de objetos en tiempo real. Desarrollado por Joseph Redmon, YOLO es conocido por su rapidez y precisión al identificar y localizar objetos en imágenes y videos en una sola pasada por la red neuronal, lo que lo hace muy eficiente para aplicaciones en tiempo real como la vigilancia, la conducción autónoma y la robótica. Este algoritmo ha sido recomendado para el profesor de prácticas de Visión por Computador.
### Ejemplos del algoritmo Yolo
| Ejemplo 1 | Ejemplo 2 |
| --- | --- |
| ![yolo_example_1](image/README/yolo_example_1.jpeg) | ![yolo_example_2](image/README/yolo_example_2.jpeg) |

### Aplicación en la KAneda-JFG

**Captura de Imagen:** La moto está equipada con una cámara de la raspberry pi que capturará imagenes en tiempo real.

**Procesamiento de Imagen:** Las imagenes capturadas se pasan al algoritmo YOLO, que detecta y clasifica las señales de tráfico presentes en la imagen.

**Identificación de Señales** YOLO puede detectar diversas señales de tráfico como "Stop", "Límite de Velocidad", "Ceda el Paso", "No Estacionar", entre otras.

**Reacción de la Moto** Dependiendo de la señal detectada, la moto tomará diferentes acciones. 

**El ejemplo que queremos aplicar:**

**Señal de Stop:** La moto reducirá la velocidad y se detendrá completamente.

**Límite de Velocidad:** La moto ajustará su velocidad para cumplir con el límite indicado.

**Ceda el Paso:** La moto reducirá la velocidad y esperará hasta que sea seguro avanzar.

## Simulación

## Contribuciones y Agradecimientos

## Autoría

| Nombre | NIU | Cargo |
| --- | --- | --- |
| Francesc Gallego Palomo | 1467414 | Responsable de Visión por Computador |
| Göran Hatero Comino | 1600920 | Responsable de Software |
| Aleix Valdivieso González | 1522975 | Responsable de Diseño 3D |
| Jordi Pradas López | 1599977 | Responsable de Hardware |

## Bibliografía
