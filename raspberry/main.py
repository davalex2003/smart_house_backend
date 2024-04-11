import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
import os
import requests

Movement_detected = False
camera = PiCamera(resolution=(800, 600))
camera.shutter_speed = 60000
camera.iso = 200

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)


def detected_callback():
    global Movement_detected
    Movement_detected = True
    print("Movement detected!")


GPIO.add_event_detect(7, GPIO.RISING, callback=detected_callback)

url = "http://192.168.1.19:8000/security/raspberry"

try:
    while True:
        if Movement_detected:
            try:
                filename = os.path.join('192.168.1.9.png')
                camera.capture(filename)
                files = {"image": open("192.168.1.9.png", "rb")}
                requests.post(url, files=files)
            except Exception as E:
                print(f'** Error {E} **')
                pass
            Movement_detected = False
        sleep(0.1)
except KeyboardInterrupt:
    camera.close()
    GPIO.cleanup()

camera.close()
GPIO.cleanup()
