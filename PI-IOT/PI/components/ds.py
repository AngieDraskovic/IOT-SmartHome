import json
import threading
import time
from datetime import datetime, timedelta

import paho.mqtt.publish as publish

from broker_settings import HOSTNAME, PORT
from simulators.ds import run_ds_simulator

# DOOR SENSOR

ds_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

door_open_times = {1: None, 2: None}
alarm_triggered_by = {1: False, 2: False}


def publisher_task(event, ds_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()  # ceka na signal za slanje podataka
        with counter_lock:
            local_ds_batch = ds_batch.copy()  # bezbjedno (sa counter lockom) preuzima podatke i prazni orginal za nove
            publish_data_counter = 0
            ds_batch.clear()
        publish.multiple(local_ds_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} ds values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ds_batch,))
publisher_thread.daemon = True  # nit ce se automatski zatvoriti kad se zatvori glavni program
publisher_thread.start()


def door_sensor_callback(status, publish_event, ds_settings, code="DSLIB_OK", verbose=True):
    global publish_data_counter, publish_data_limit, door_open_times
    value = 1 if status == "open" else 0
    now = datetime.utcnow().isoformat()
    sensor_id = ds_settings["id"]
    current_time = datetime.utcnow()
    if verbose:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Door Status: {status} = {value}")
        print("=" * 20)

    status_payload = {
        "measurement": "Door Status",
        "simulated": ds_settings['simulated'],
        "runs_on": ds_settings["runs_on"],
        "name": ds_settings["name"],
        "timestamp": now,
        "value": value
    }
    message_for_front_CP = {"room": "COVERED PORCH-DS", "door_sensor": False}
    message_for_front_G = {"room": "GARAGE-DS", "door_sensor": False}

    if status == "open":
        if door_open_times[sensor_id] is None:
            door_open_times[sensor_id] = current_time
    else:
        if alarm_triggered_by[sensor_id]:
            deactivate_alarm(sensor_id)
            alarm_triggered_by[sensor_id] = False
        door_open_times[sensor_id] = None

    if door_open_times[sensor_id] and (current_time - door_open_times[sensor_id] > timedelta(seconds=5)):
        if not alarm_triggered_by[sensor_id]:
            activate_alarm(sensor_id)
            alarm_triggered_by[sensor_id] = True

    if sensor_id == 1:
        message_for_front_CP["door_sensor"] = status
        publish.single("frontend/update", payload=json.dumps(message_for_front_CP), hostname=HOSTNAME, port=PORT)
    else:
        message_for_front_G["door_sensor"] = status
        publish.single("frontend/update", payload=json.dumps(message_for_front_G), hostname=HOSTNAME, port=PORT)

    with counter_lock:
        ds_batch.append(('Door Status', json.dumps(status_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def activate_alarm(sensor_id):
    alarm_message = {f"DS{sensor_id}": True}
    topic = "home/alarm/activate"
    print(f"Alarm activation message sent (ds{sensor_id}).")
    publish.single(topic, json.dumps(alarm_message), hostname=HOSTNAME, port=PORT)


def deactivate_alarm(sensor_id):
    alarm_message = {f"DS{sensor_id}": True}
    topic = "home/alarm/deactivate"
    print(f"Alarm deactivation message sent(ds{sensor_id}).")
    publish.single(topic, json.dumps(alarm_message), hostname=HOSTNAME, port=PORT)


def run_door_sensor_simulator(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        ds_thread = threading.Thread(target=run_ds_simulator,
                                     args=(3, door_sensor_callback, stop_event, publish_event, settings))
        ds_thread.start()
        threads.append(ds_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.ds import run_door_sensor_loop, DS
        print(f"Starting  {settings['name']} loop")
        ds = DS(settings['pin'], publish_event, door_sensor_callback, settings)
        ds_thread = threading.Thread(target=run_door_sensor_loop,
                                     args=(1, ds, door_sensor_callback, stop_event, publish_event, settings))
        ds_thread.start()
        threads.append(ds_thread)
        print(f" {settings['name']} loop started")
