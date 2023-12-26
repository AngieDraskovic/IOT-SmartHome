import threading
import time
import json
from PI1.simulators.dpir1 import run_dpir1_simulator
from broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
from datetime import datetime

# DOOR MOTION SENSOR
dpir1_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()



def publisher_task(event, dpir1_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()    # ceka na signal za slanje podataka
        with counter_lock:
            local_dpir1_batch = dpir1_batch.copy()  # bezbjedno (sa counter lockom) preuzima podatke i prazni orginal za nove
            publish_data_counter = 0
            dpir1_batch.clear()
        publish.multiple(local_dpir1_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} ds1 values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dpir1_batch,))
publisher_thread.daemon = True  # nit ce se automatski zatvoriti kad se zatvori glavni program
publisher_thread.start()




def door_motion_callback(motion, publish_event, dpir1_settings, code="DPIR1LIB_OK", verbose=True):
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
        "simulated": dpir1_settings['simulated'],
        "runs_on": dpir1_settings["runs_on"],
        "name": dpir1_settings["name"],
        "timestamp": now,
        "value": value
    }

    with counter_lock:
        dpir1_batch.append(('Door Motion Sensor', json.dumps(status_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()






def run_door_motion_sensor_simulator(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DPIR1 simulator")
        dpir1_thread = threading.Thread(target=run_dpir1_simulator, args=(2, door_motion_callback, stop_event, publish_event, settings))
        dpir1_thread.start()
        threads.append(dpir1_thread)
    else:
        from PI1.sensors.dpir1 import run_door_montion_sensor_loop, DPIR1
        print("Starting DPIR1 loop")
        dpir1 = DPIR1(settings['pin'], publish_event, door_motion_callback, settings)
        dpir1_thread = threading.Thread(target=run_door_montion_sensor_loop, args=(dpir1, 2, stop_event))
        dpir1_thread.start()

        threads.append(dpir1_thread)


