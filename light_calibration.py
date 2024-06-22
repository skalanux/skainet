import cv2
import numpy as np
import time

def is_light_on(frame, threshold=250, min_brightness_area=23500):
    # Convertir el frame a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar un umbral para detectar las áreas brillantes
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    # Encontrar los contornos de las áreas brillantes
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Calcular el área total de las regiones brillantes
    bright_area = sum(cv2.contourArea(contour) for contour in contours)
    
    # Determinar si la luz está encendida o apagada
    light_on = bright_area > min_brightness_area
    
    return light_on, bright_area, thresh

# Capturar el video desde la cámara
cap = cv2.VideoCapture(0)  # Cambiar el índice si hay más de una cámara

last_checked_time = time.time()
check_interval =  0.1 # Intervalo de tiempo para verificar el estado de la luz en segundos

cant_lights = 0
cant_darks = 0
light_prev=False


while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    current_time = time.time()
    if True: #current_time - last_checked_time >= check_interval:
        light_on, bright_area, thresh = is_light_on(frame)
        delta_time = current_time - last_checked_time
        last_checked_time = current_time
        cv2.imshow("Frame", frame)
        cv2.imshow("Threshold", thresh)

        if light_on != light_prev:
            if light_on:
                if cant_darks<40:
                    print("")
                else:
                    print("//")
            else:
                if cant_lights<8:
                    print(".")
                else:
                    print("-")
                #print(f"{delta_time:.3f}: cant_lights:{cant_lights} cant_darks:{cant_darks}")
            light_prev = light_on
            cant_lights=0
            cant_darks=0

        if light_on:
            cant_lights+=1
        else:
            cant_darks+=1


    # Salir del loop si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar el objeto de captura y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()

