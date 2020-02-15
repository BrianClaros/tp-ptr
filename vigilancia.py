# Importamos las librerías necesarias
import numpy as np
import cv2
import time
import pickle
import serverEmail as srEmail
from utils import obtenerPorcentajeDeDiferencia
import datetime
import imutils
import argparse

ENVIAR_DESP_DE_SEG = 60

#Construccion de analizador de argumentos y analizar los argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

#inicio de server email
email = srEmail.ServerEmail('smtp.gmail.com','587','facedetectionunaj@gmail.com','prog_real1')
emailSend = False
time_reset_flag = None

# Cargamos el vídeo
web_cam = cv2.VideoCapture(0)

# Inicializamos el primer frame a vacío.
# Nos servirá para obtener el fondo
fondo = None

# Recorremos todos los frames
while True:
    # Obtenemos el frame
    (grabbed, frame) = web_cam.read()

    # Texto para indicar si hubo in ingreso de alguien
    text = "Desocupado"

    # Si hemos llegado al final del vídeo salimos
    if not grabbed:
        break


    #ajustamos el tamaño del frame
    frame = imutils.resize(frame,width=500)
    # Convertimos a escala de grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicamos suavizado para eliminar ruido
    gris = cv2.GaussianBlur(gris, (21, 21), 0)

    # Si todavía no hemos obtenido el fondo, lo obtenemos
    # Será el primer frame que obtengamos
    if fondo is None:
        fondo = gris
        continue

    # Reseteamos el flag y asignamos una nueva imagen al fondo para mantenerlo
    # actualizado
    if emailSend is True and time.time() >= time_reset_flag:
        time_reset_flag = None
        fondo = gris
        emailSend = False
        continue

    # Calculo de la diferencia entre el fondo y el frame actual
    resta = cv2.absdiff(fondo, gris)

    # Aplicamos un umbral
    umbral = cv2.threshold(resta, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilatamos el umbral para tapar agujeros
    umbral = cv2.dilate(umbral, None, iterations=2)

    # Copiamos el umbral para detectar los contornos
    contornosimg = umbral.copy()

    # Buscamos contorno en la imagen
    contornos = cv2.findContours(contornosimg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    contornos = imutils.grab_contours(contornos)

    # Recorremos todos los contornos encontrados
    for c in contornos:
        # Eliminamos los contornos más pequeños
        if cv2.contourArea(c) < args["min_area"]:
            continue

        #Calcular el cuadro delimitador para el contorno, dibujarlo en el marco y actualizar el texto
        text = "Ocupado"
        if emailSend == False:
            time.sleep(3)
            return_value, image = web_cam.read()
            imageName = 'screenshot.jpg'
            cv2.imwrite(imageName, image)
            email.sendMsjImage('facedetectionunaj@gmail.com', 'ALERTA', imageName)
            time_reset_flag = time.time() + ENVIAR_DESP_DE_SEG
            emailSend = True


    cv2.putText(frame, "Estado de aula: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # Mostramos las imágenes de la cámara, el umbral y la resta
    cv2.imshow("Camara", frame)

    # Capturamos una tecla para salir
    key = cv2.waitKey(1) & 0xFF

    # Si ha pulsado la letra s, salimos
    if key == ord("s"):
        break

# Paramos el servidor de emails
email.stopServerEmail()

# Liberamos la cámara y cerramos todas las ventanas
web_cam.release()
cv2.destroyAllWindows()
