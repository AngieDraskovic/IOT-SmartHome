import json
import threading
import time
from datetime import datetime
import paho.mqtt.publish as publish
from simulators.bir import run_bir_simulator
from broker_settings import HOSTNAME, PORT


bir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, bir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_bir_batch = bir_batch.copy()
            publish_data_counter = 0
            bir_batch.clear()
        publish.multiple(local_bir_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {len(local_bir_batch)} BIR values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, bir_batch))
publisher_thread.daemon = True
publisher_thread.start()


def bir_callback(code, publish_event, bir_settings, verbose=True):
    global publish_data_counter, publish_data_limit
    now = datetime.utcnow().isoformat()
    if verbose:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"{bir_settings['name']} code: {code}")
        print("=" * 20)
    payload = {
        "measurement": "Bedroom Infrared",
        "simulated": bir_settings['simulated'],
        "runs_on": bir_settings["runs_on"],
        "name": bir_settings["name"],
        "timestamp": now,
        "value": code,
    }

    with counter_lock:
        # Objavljivanje podataka u okviru "home/dht" topika
        bir_batch.append(('Bedroom Infrared', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

    topic = f"sensor/bir"
    payload = json.dumps({"button_pressed": code})
    publish.single(topic, payload=payload, hostname=HOSTNAME, port=PORT)
    message_for_front = {"room": "OWNER SUITE-BIR", "button_pressed": code}
    publish.single("frontend/update", payload=json.dumps(message_for_front), hostname=HOSTNAME, port=PORT)


def run_bir(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting " + settings["name"] + " simulator")
        bir_thread = threading.Thread(target=run_bir_simulator, args=(5, bir_callback, stop_event, publish_event, settings))
        bir_thread.start()
        threads.append(bir_thread)
        print(settings["name"] + " sumilator started")
    else:
        from sensors.bir import run_bir_loop
        print("Starting " + settings["name"] + " loop")
        bir_thread = threading.Thread(target=run_bir_loop, args=(bir_callback, stop_event, publish_event, settings))
        bir_thread.start()
        threads.append(bir_thread)
        print(settings["name"] + " loop started")