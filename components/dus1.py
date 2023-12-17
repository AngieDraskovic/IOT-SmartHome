import threading
from simulators.dus1 import run_dus1_simulator
import time
from components.utilites import print_lock
from broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
from datetime import datetime
import json
# DOOR ULTRASONIC SENSOR
dus1_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, dus1_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()    # ceka na signal za slanje podataka
        with counter_lock:
            local_dus1_batch = dus1_batch.copy()
            publish_data_counter = 0
            dus1_batch.clear()
        publish.multiple(local_dus1_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dus1 values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dus1_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dus1_callback(value, publish_event, dus1_settings, code="DUS1LIB_OK", verbose=True):
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
        "simulated": dus1_settings['simulated'],
        "runs_on": dus1_settings["runs_on"],
        "name": dus1_settings["name"],
        "timestamp": now,
        "value": float(value)
    }

    with counter_lock:
        dus1_batch.append(('Door Ultrasonic Sensor', json.dumps(status_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_door_ultrasonic_simulator(settings, threads, stop_event ):
    if settings['simulated']:
        print("Starting DUS1 simulator")
        dus1_thread = threading.Thread(target=run_dus1_simulator, args=(5, dus1_callback, stop_event, publish_event, settings))
        dus1_thread.start()
        threads.append(dus1_thread)
        print("DUSS1 simulator started")
    else:
        from sensors.dus1 import run_ultrasonic_sensor_loop, DUS1
        print("Starting DUS1 loop")
        dus1 = DUS1(settings['pin_trig'], settings['pin_echo'])
        dus1_thread = threading.Thread(target=run_ultrasonic_sensor_loop, args=(5, dus1, dus1_callback, stop_event))
        dus1_thread.start()
        threads.append(dus1_thread)
        print("DUS1 loop started")