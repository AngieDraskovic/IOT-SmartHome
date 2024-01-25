import json
import threading

import time
from datetime import datetime
from actuators.brgb import brgb
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT
from paho.mqtt import publish

mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, PORT)
mqtt_client.subscribe("sensor/bir")
mqtt_client.subscribe("server/button_pressed")
mqtt_client.loop_start()

brgb_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

button_pressed = '0'


def on_message(client, userdata, message):
    global button_pressed
    data = json.loads(message.payload)
    button_pressed = data["button_pressed"]


mqtt_client.on_message = on_message


def publisher_task(event, brgb_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_brgb_batch = brgb_batch.copy()
            publish_data_counter = 0
            brgb_batch.clear()
        publish.multiple(local_brgb_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {len(local_brgb_batch)} BRGB values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, brgb_batch))
publisher_thread.daemon = True
publisher_thread.start()


def brgb_simul(settings, publish_event):
    global publish_data_counter, publish_data_limit
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
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": now,
        "value": color,
    }

    message_for_front = {"room": "COVERED PORCH-BRGB", "color": color}
    publish.single("frontend/update",  payload=json.dumps(message_for_front), hostname=HOSTNAME, port=PORT)
    with counter_lock:
        brgb_batch.append(('Bedroom RGB', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_brgb(settings, stop_event):
    try:
        while not stop_event.is_set():  # Provjera da li je stop_event setovan
            if settings['simulated']:
                brgb_simul(settings, publish_event)
                time.sleep(1)
            else:
                brgb(settings, button_pressed)
                time.sleep(1)

    except KeyboardInterrupt:
        print("Ending BRGB")
    finally:
        print("BRGB thread is stopping")