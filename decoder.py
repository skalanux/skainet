import logging
import queue
import threading
import time

import cv2
from morse_equivs import equivs


INTERVAL_BETWEEN_WORDS = (13,20)
INTERVAL_BETWEEN_SYMBOLS = (6,12)
LIGHT_INTERVAL_DOT = (1,7)
LIGHT_INTERVAL_DASH = (8,20)


def _is_light_on(frame, threshold=250, min_brightness_area=23500):
    """Check wether light is on or off."""
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


def _write_to_queue(morse_queue, char):
    """Write results to queue, so it can be displayed on console."""
    morse_queue.put(char)


def show_queue(morse_queue):
    while True:

        print(morse_queue.get(), end='', flush=True)
        time.sleep(0.3)


def scan(morse_queue, command_queue=None):
    """Scan camera."""
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    cant_lights = 0
    cant_darks = 0
    symbols = ''

    print_space = False
    print_symbol = False

    logging.debug("Decoding...")

    capture_code = True

    while True:
        if command_queue is not None and len(command_queue) > 0:

            command = command_queue.pop()

            if command=='TOGGLE':
                if capture_code:
                    logging.debug("Stopping...")
                    capture_code = False
                    cap.release()
                else:
                    logging.debug("Starting...")
                    cap = cv2.VideoCapture(0)  # Cambiar el índice si hay más de una cámara
                    capture_code = True

        if not capture_code:
            time.sleep(1)
            continue

        ret, frame = cap.read()
        if not ret:
            break
        
        light_on, bright_area, thresh = _is_light_on(frame)


        print_space = False
        print_symbol = False

        if light_on:
            cant_lights+=1
            if cant_darks>0:
                if cant_darks in range(*INTERVAL_BETWEEN_WORDS):
                    print_space = True
                    print_symbol = True
                elif cant_darks in range(*INTERVAL_BETWEEN_SYMBOLS):
                    print_symbol = True

            cant_darks=0
        else:
            cant_darks+=1
            if cant_lights>0:
                if cant_lights in range(*LIGHT_INTERVAL_DOT):
                    symbols+='.'
                elif cant_lights in range(*LIGHT_INTERVAL_DASH):
                    symbols+='-'

            cant_lights=0
       
            if cant_darks > INTERVAL_BETWEEN_WORDS[1] and symbols:
                print_symbol = True
                #keep_scanning = False

        if print_symbol:
            logging.debug(f"{symbols}: {equivs.get(symbols)}")
            letter=equivs.get(symbols)
            _write_to_queue(morse_queue, letter)
            symbols=''
        if print_space:
            logging.debug(f"\\")
            _write_to_queue(morse_queue, ' ')
            symbols=''

        # show original frame and threshold
        #cv2.imshow("Frame", frame)
        #cv2.imshow("Threshold", thresh)

    # Liberar el objeto de captura y cerrar todas las ventanas
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    morse_queue = queue.Queue()
    scan_thread = threading.Thread(target=show_queue, args=(morse_queue,))
    scan_thread.daemon = True
    scan_thread.start()
    scan(morse_queue)
    morse_queue.join()
