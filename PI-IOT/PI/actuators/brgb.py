import json

from paho.mqtt import publish
from broker_settings import HOSTNAME, PORT
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
except:
    pass
from time import sleep
from datetime import datetime



def turnOff(device):
    GPIO.output(device["RED_PIN"], GPIO.LOW)
    GPIO.output(device["GREEN_PIN"], GPIO.LOW)
    GPIO.output(device["BLUE_PIN"], GPIO.LOW)


def white(device):
    GPIO.output(device["RED_PIN"], GPIO.HIGH)
    GPIO.output(device["GREEN_PIN"], GPIO.HIGH)
    GPIO.output(device["BLUE_PIN"], GPIO.HIGH)


def red(device):
    GPIO.output(device["RED_PIN"], GPIO.HIGH)
    GPIO.output(device["GREEN_PIN"], GPIO.LOW)
    GPIO.output(device["BLUE_PIN"], GPIO.LOW)


def green(device):
    GPIO.output(device["RED_PIN"], GPIO.LOW)
    GPIO.output(device["GREEN_PIN"], GPIO.HIGH)
    GPIO.output(device["BLUE_PIN"], GPIO.LOW)


def blue(device):
    GPIO.output(device["RED_PIN"], GPIO.LOW)
    GPIO.output(device["GREEN_PIN"], GPIO.LOW)
    GPIO.output(device["BLUE_PIN"], GPIO.HIGH)


def yellow(device):
    GPIO.output(device["RED_PIN"], GPIO.HIGH)
    GPIO.output(device["GREEN_PIN"], GPIO.HIGH)
    GPIO.output(device["BLUE_PIN"], GPIO.LOW)


def purple(device):
    GPIO.output(device["RED_PIN"], GPIO.HIGH)
    GPIO.output(device["GREEN_PIN"], GPIO.LOW)
    GPIO.output(device["BLUE_PIN"], GPIO.HIGH)


def lightBlue(device):
    GPIO.output(device["RED_PIN"], GPIO.LOW)
    GPIO.output(device["GREEN_PIN"], GPIO.HIGH)
    GPIO.output(device["BLUE_PIN"], GPIO.HIGH)


def set_color(value):
    color = value


def brgb(device, button_pressed):
    now = datetime.utcnow().isoformat()
    color = "TURNED OFF"
    if button_pressed == '0':
        print("TURNED OFF")
        color = "TURNED OFF"
    elif button_pressed == '1':
        print("white")
        color = "white"
    elif button_pressed == '2':
        print("red")
        color = "red"
    elif button_pressed == '3':
        print("green")
        color = "green"
    elif button_pressed == '4':
        print("blue")
        color = "blue"
    elif button_pressed == '5':
        print("yellow")
        color = "yellow"
    elif button_pressed == '6':
        print("purple")
        color = "purple"
    elif button_pressed == '7':
        print("light blue")
        color = "light blue"
    payload = {
        "measurement": "Bedroom RGB",
        "simulated": device['simulated'],
        "runs_on": device["runs_on"],
        "name": device["name"],
        "timestamp": now,
        "value": color,
    }
    publish.single("Bedroom RGB", payload=json.dumps(payload), hostname=HOSTNAME, port=PORT)
    message_for_front = {"room": "COVERED PORCH-BRGB", "color": color}
    publish.single("frontend/update", payload=json.dumps(message_for_front), hostname=HOSTNAME, port=PORT)
    try:
        GPIO.setup(device["RED_PIN"], GPIO.OUT)
        GPIO.setup(device["GREEN_PIN"], GPIO.OUT)
        GPIO.setup(device["BLUE_PIN"], GPIO.OUT)
        while True:
            if color == 'TURNED OFF':
                turnOff(device)
            elif color == 'white':
                white(device)
            elif color == 'red':
                red(device)
            elif color == 'green':
                green(device)
            elif color == 'blue':
                blue(device)
            elif color == 'yellow':
                yellow(device)
            elif color == 'purple':
                purple(device)
            elif color == 'light_blue':
                lightBlue(device)

    except KeyboardInterrupt:
        GPIO.cleanup()