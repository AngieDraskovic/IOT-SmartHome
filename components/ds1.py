import threading
import time
import json
from simulators.ds1 import run_ds_simulator
from broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
from datetime import datetime
# DOOR SENSOR

ds1_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, ds1_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()    # ceka na signal za slanje podataka
        with counter_lock:
            local_ds1_batch = ds1_batch.copy()  # bezbjedno (sa counter lockom) preuzima podatke i prazni orginal za nove
            publish_data_counter = 0
            ds1_batch.clear()
        publish.multiple(local_ds1_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} ds1 values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ds1_batch,))
publisher_thread.daemon = True  # nit ce se automatski zatvoriti kad se zatvori glavni program
publisher_thread.start()


def door_sensor_callback(status, publish_event, ds1_settings, code="DS1LIB_OK", verbose=True):
    global publish_data_counter, publish_data_limit
    value = 1 if status == "open" else 0
    now = datetime.utcnow().isoformat()
    if verbose:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Door Status: {status} = {value}")
        print("=" * 20)

    status_payload = {
        "measurement": "Door Status",
        "simulated": ds1_settings['simulated'],
        "runs_on": ds1_settings["runs_on"],
        "name": ds1_settings["name"],
        "timestamp": now,
        "value": value
    }

    with counter_lock:
        ds1_batch.append(('Door Status', json.dumps(status_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_door_sensor_simulator(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DS simulator")
        ds1_thread = threading.Thread(target=run_ds_simulator, args=(3, door_sensor_callback, stop_event, publish_event, settings))
        ds1_thread.start()
        threads.append(ds1_thread)
        print("DS1 simulator started")
    else:
        from sensors.ds1 import run_door_sensor_loop, DS1
        print("Starting DS1 loop")
        ds1 = DS1(settings['pin'], door_sensor_callback)
        ds1_thread = threading.Thread(target=run_door_sensor_loop, args=(ds1, 3, door_sensor_callback, stop_event, publish_event, settings))
        ds1_thread.start()
        threads.append(ds1_thread)
        print("DS1 loop started")
