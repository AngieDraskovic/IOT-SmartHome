import json
import threading
import time
from datetime import datetime

import paho.mqtt.publish as publish

from broker_settings import HOSTNAME, PORT
from simulators.dpir import run_dpir_simulator

# DOOR MOTION SENSOR
dpir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()



def publisher_task(event, dpir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()    # ceka na signal za slanje podataka
        with counter_lock:
            local_dpir_batch = dpir_batch.copy()  # bezbjedno (sa counter lockom) preuzima podatke i prazni orginal za nove
            publish_data_counter = 0
            dpir_batch.clear()
        publish.multiple(local_dpir_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dpir values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dpir_batch,))
publisher_thread.daemon = True  # nit ce se automatski zatvoriti kad se zatvori glavni program
publisher_thread.start()




def door_motion_callback(motion, publish_event, dpir_settings, code="DPIRLIB_OK", verbose=True):
    global publish_data_counter, publish_data_limit
    value = 1 if motion else 0
    now = datetime.utcnow().isoformat()
    if verbose:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Door Motion Sensor: {str(motion)} = {value}")
        print("=" * 20)

    status_payload = {
        "measurement": "Door Motion Sensor",
        "simulated": dpir_settings['simulated'],
        "runs_on": dpir_settings["runs_on"],
        "name": dpir_settings["name"],
        "timestamp": now,
        "value": value
    }

    with counter_lock:
        dpir_batch.append(('Door Motion Sensor', json.dumps(status_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()




def run_door_motion_sensor_simulator(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        dpir_thread = threading.Thread(target=run_dpir_simulator, args=(2, door_motion_callback, stop_event, publish_event, settings))
        dpir_thread.start()
        threads.append(dpir_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.dpir import run_door_montion_sensor_loop, DPIR
        print(f"Starting {settings['name']} loop")
        dpir = DPIR(settings['pin'], publish_event, door_motion_callback, settings)
        dpir_thread = threading.Thread(target=run_door_montion_sensor_loop, args=(2, dpir, stop_event))
        dpir_thread.start()
        print(f"{settings['name']} loop started")
        threads.append(dpir_thread)


