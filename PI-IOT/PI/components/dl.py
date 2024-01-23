import json
from datetime import datetime
import time
import paho.mqtt.publish as publish
import threading
from components.dpir import light_event
from .utilites import *
from broker_settings import HOSTNAME, PORT

light_batch = []
light_data_counter = 0
light_data_limit = 5
light_counter_lock = threading.Lock()

def write_to_database(value, settings, publisher):
    light_payload = {
        "measurement": "Door Light",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": datetime.utcnow().isoformat(),
        "value": value
    }
    publisher.add_values(['Door Light'], [light_payload])


def light_publisher_task(event, light_batch):
    global light_data_counter, light_data_limit
    while True:
        event.wait()  # čeka na signal za slanje podataka
        with light_counter_lock:
            local_light_batch = light_batch.copy()
            light_data_counter = 0
            light_batch.clear()
        publish.multiple(local_light_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {light_data_limit} light values')
        event.clear()


light_publish_event = threading.Event()
light_publisher_thread = threading.Thread(target=light_publisher_task, args=(light_publish_event, light_batch,))
light_publisher_thread.daemon = True
light_publisher_thread.start()

def handle_door_light(settings):
    global light_data_counter, light_data_limit, door_light_state
    door_light = None
    if not settings['simulated']:
        from actuators.dl import DL
        door_light = DL(settings['pin'])
    publisher = Publisher()
    message_for_front_CP = {"room":"LIGHT DATA", "light_on": False}
    try:
        while True:
            if settings['simulated']:
                light_event.wait()
                door_light_state = True

                message_for_front_CP["light_on"] = True
                publish.single("frontend/update", payload=json.dumps(message_for_front_CP), hostname=HOSTNAME,
                               port=PORT)
                print(f"Door Light turned ON")
                write_to_database(1, settings, publisher)  # 1 jer sam upalila
                start_time = time.time()
                while time.time() - start_time < 10:
                    if light_event.is_set():
                        start_time = time.time()  # resetovanje timera
                        light_event.clear()
                    time.sleep(0.5)

                # Toggle the light state to off after 10 seconds
                if door_light_state:
                    door_light_state = False
                    message_for_front_CP["light_on"] = False
                    publish.single("frontend/update", payload=json.dumps(message_for_front_CP), hostname=HOSTNAME,
                                   port=PORT)
                    print("Door Light turned OFF")

                    write_to_database(0, settings, publisher)

                light_event.clear()
            else:
                light_event.wait()  # Wait for the motion detection event

                door_light.turn_on(write_to_database, settings, publisher)

                # ostavljam svjetlo 10 sekundi upaljeno
                start_time = time.time()
                while time.time() - start_time < 10:
                    if light_event.is_set():
                        start_time = time.time()    # resetovanje timera ako se opet desi motion
                        light_event.clear()
                    time.sleep(0.5)  # kratki sleep zbog Cpu

                # ugasi svjetlo poslije 10 sekundi
                if door_light and door_light.get_state():
                    door_light.turn_off(write_to_database, settings, publisher)

                light_event.clear()
    except KeyboardInterrupt:
        print("Ending Door Light control")
    finally:
        if door_light:
            door_light.cleanup()
