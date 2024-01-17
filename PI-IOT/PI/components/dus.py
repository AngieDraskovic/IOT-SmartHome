import json
import threading
import time
from datetime import datetime

import paho.mqtt.publish as publish

from broker_settings import HOSTNAME, PORT
from simulators.dus import run_dus_simulator

# DOOR ULTRASONIC SENSOR
dus_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, dus_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()    # ceka na signal za slanje podataka
        with counter_lock:
            local_dus_batch = dus_batch.copy()
            publish_data_counter = 0
            dus_batch.clear()
        publish.multiple(local_dus_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dus values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dus_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dus_callback(value, publish_event, dus_settings, code="DUSLIB_OK", verbose=True):
    global publish_data_counter, publish_data_limit
    now = datetime.utcnow().isoformat()
    if verbose:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Door Ultrasonic Sensor: {value}")
        print("=" * 20)

    status_payload = {
        "measurement": "Door Ultrasonic Sensor",
        "simulated": dus_settings['simulated'],
        "runs_on": dus_settings["runs_on"],
        "name": dus_settings["name"],
        "timestamp": now,
        "value": float(value)
    }

    with counter_lock:
        dus_batch.append(('Door Ultrasonic Sensor', json.dumps(status_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_door_ultrasonic_simulator(settings, threads, stop_event ):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        dus_thread = threading.Thread(target=run_dus_simulator, args=(5, dus_callback, stop_event, publish_event, settings))
        dus_thread.start()
        threads.append(dus_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.dus import run_ultrasonic_sensor_loop, DUS
        print(f"Starting {settings['name']} loop")
        dus = DUS(settings['pin_trig'], settings['pin_echo'])
        dus_thread = threading.Thread(target=run_ultrasonic_sensor_loop, args=(5, dus, dus_callback, stop_event, publish_event, settings))
        dus_thread.start()
        threads.append(dus_thread)
        print(f"{settings['name']} loop started")