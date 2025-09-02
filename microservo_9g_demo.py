# PIN list:
#
# PIN | GPIO | Conexión
# ----+------+------------
#  D1 |   5  | Servo dedo índice
#  D2 |   4  | Servo dedo corazón
#  D5 |  14  | Tira LED
#  D6 |  12  | Servo dedo meñique
#  D7 |  13  | Servo dedo anular

import machine
import neopixel
import time
import math
from machine import Pin, PWM

# Configuración de pines según la lista
PIN_LED = 14        # D5 - Tira LED
PIN_MENIQUE = 12    # D6 - Servo dedo meñique
PIN_ANULAR = 13     # D7 - Servo dedo anular
PIN_CORAZON = 4     # D2 - Servo dedo corazón
PIN_INDICE = 5      # D1 - Servo dedo índice

NUM_LEDS = 4

# Inicializar la tira LED
strip = neopixel.NeoPixel(machine.Pin(PIN_LED), NUM_LEDS)

# Inicializar servos
servo_menique = PWM(Pin(PIN_MENIQUE))
servo_anular = PWM(Pin(PIN_ANULAR))
servo_corazon = PWM(Pin(PIN_CORAZON))
servo_indice = PWM(Pin(PIN_INDICE))

# Configurar frecuencia de servos
for servo in [servo_menique, servo_anular, servo_corazon, servo_indice]:
    servo.freq(50)

def clear_all():
    """Apaga todos los LEDs"""
    for i in range(NUM_LEDS):
        strip[i] = (0, 0, 0)
    strip.write()

def set_all_white():
    """Pone todos los LEDs en blanco"""
    for i in range(NUM_LEDS):
        strip[i] = (255, 255, 255)
    strip.write()

def angle_servo(servo, deg, us_min=600, us_max=2400):
    """Mueve el servo al ángulo especificado"""
    deg = max(0, min(180, deg))
    us = us_min + (us_max - us_min) * deg / 180
    servo.duty_ns(int(us * 1000))

def servo_sweep(servo, duration=5.0):
    """Hace la progresión de 0º a 180º ida y vuelta"""
    steps = 180
    delay = duration / (steps * 2)
    
    # Ida (0 a 180)
    for a in range(0, 181):
        angle_servo(servo, a)
        time.sleep(delay)
    
    # Vuelta (180 a 0)
    for a in range(179, -1, -1):
        angle_servo(servo, a)
        time.sleep(delay)

def hsv_to_rgb(h, s, v):
    """Convierte HSV a RGB"""
    h = h / 255.0 * 360
    s = s / 255.0
    v = v / 255.0
    
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

def step_1_parpadeo_rojo():
    """1. Parpadean todos los LEDs en ROJO durante 1 segundo"""
    print("Paso 1: Parpadeo rojo")
    start_time = time.time()
    state = True
    
    while time.time() - start_time < 1.0:
        if state:
            for i in range(NUM_LEDS):
                strip[i] = (255, 0, 0)  # Rojo
        else:
            clear_all()
        strip.write()
        state = not state
        time.sleep(0.1)  # Parpadeo cada 0.1 segundos

def step_2_menique():
    """2. LEDs blancos y meñique hace progresión"""
    print("Paso 2: LEDs blancos + servo meñique")
    set_all_white()
    servo_sweep(servo_menique)

def step_3_secuencia_colores():
    """3. LEDs en secuencia R, G, B, Blanco durante 1 segundo"""
    print("Paso 3: Secuencia de colores")
    colors = [
        (255, 0, 0),    # Rojo
        (0, 255, 0),    # Verde
        (0, 0, 255),    # Azul
        (255, 255, 255) # Blanco
    ]
    
    start_time = time.time()
    flash_duration = 1.0/12.0  # 1/12 de segundo
    
    while time.time() - start_time < 1.0:
        for i in range(NUM_LEDS):
            clear_all()
            strip[i] = colors[i]
            strip.write()
            time.sleep(flash_duration)

def step_4_anular():
    """4. LEDs blancos y anular hace progresión"""
    print("Paso 4: LEDs blancos + servo anular")
    set_all_white()
    servo_sweep(servo_anular)

def step_5_discoteca():
    """5. Efecto discoteca durante 1 segundo"""
    print("Paso 5: Efecto discoteca")
    start_time = time.time()
    
    while time.time() - start_time < 1.0:
        # Cambio rápido de colores tipo discoteca
        hue = int((time.time() - start_time) * 500) % 256  # Cambio rápido
        for i in range(NUM_LEDS):
            # Cada LED con un matiz ligeramente diferente
            led_hue = (hue + i * 64) % 256
            strip[i] = hsv_to_rgb(led_hue, 255, 255)
        strip.write()
        time.sleep(0.02)  # Actualización rápida

def step_6_corazon():
    """6. LEDs blancos y corazón hace progresión"""
    print("Paso 6: LEDs blancos + servo corazón")
    set_all_white()
    servo_sweep(servo_corazon)

def step_7_secuencia_verde():
    """7. Ráfagas verdes en secuencia durante 1 segundo"""
    print("Paso 7: Secuencia verde")
    start_time = time.time()
    flash_duration = 1.0/12.0  # 1/12 de segundo
    
    while time.time() - start_time < 1.0:
        for i in range(NUM_LEDS):
            clear_all()
            strip[i] = (0, 255, 0)  # Verde
            strip.write()
            time.sleep(flash_duration)

def step_8_indice():
    """8. LEDs blancos y índice hace progresión"""
    print("Paso 8: LEDs blancos + servo índice")
    set_all_white()
    servo_sweep(servo_indice)

def step_9_oscilacion_infinita():
    """9. Oscilación infinita con decaimiento"""
    print("Paso 9: Oscilación infinita")
    start_time = time.time()
    
    try:
        while True:
            t = time.time() - start_time
            
            # Fórmula: (1 + 2 * cos(a·t)) / (1 + 3t)
            # Donde a se ajusta para que el período sea 1 segundo (2π/a = 1, entonces a = 2π)
            a = 2 * math.pi  # Para período de 1 segundo
            
            intensity_factor = (1 + 2 * math.cos(a * t)) / (1 + 3 * t)
            
            # Asegurar que esté entre 0 y 1
            intensity_factor = max(0, min(1, intensity_factor))
            
            # Convertir a valor de 0-255
            intensity = int(intensity_factor * 255)
            
            # Aplicar a todos los LEDs
            for i in range(NUM_LEDS):
                strip[i] = (intensity, intensity, intensity)
            strip.write()
            
            time.sleep(0.01)  # Actualización suave
            
    except KeyboardInterrupt:
        clear_all()
        print("Secuencia interrumpida")

def run_complete_sequence():
    """Ejecuta la secuencia completa"""
    print("=== INICIANDO SECUENCIA COMPLETA ===")
    
    try:
        step_1_parpadeo_rojo()
        step_2_menique()
        step_3_secuencia_colores()
        step_4_anular()
        step_5_discoteca()
        step_6_corazon()
        step_7_secuencia_verde()
        step_8_indice()
        step_9_oscilacion_infinita()
        
    except Exception as e:
        print(f"Error durante la secuencia: {e}")
        clear_all()
        # Deinicializar servos
        for servo in [servo_menique, servo_anular, servo_corazon, servo_indice]:
            servo.deinit()

# Ejecutar secuencia
if __name__ == "__main__":
    run_complete_sequence()
