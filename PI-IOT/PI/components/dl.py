import json
from datetime import datetime

import paho.mqtt.publish as publish

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
    try:
        while True:
            if settings['simulated']:
                light_event.wait()
                door_light_state = not door_light_state
                state_str = "ON" if door_light_state else "OFF"
                print(f"Door Light turned {state_str}")
                value = 1 if door_light_state else 0
                # light_payload = {
                #     "measurement": "Door Light",
                #     "simulated": settings['simulated'],
                #     "runs_on": settings["runs_on"],
                #     "name": settings["name"],
                #     "timestamp": datetime.utcnow().isoformat(),
                #     "value": value
                # }
                # BEZ PUBLISHERA
                # with light_counter_lock:
                #     light_batch.append(('Door Light', json.dumps(light_payload), 0, True))
                #     light_data_counter += 1
                #
                # if light_data_counter >= light_data_limit:
                #     light_publish_event.set()

                write_to_database(value, settings, publisher)
                light_event.clear()
            else:
                light_event.wait()

                if door_light and not door_light.get_state():
                    door_light.turn_on(write_to_database, settings, publisher)
                elif door_light and door_light.get_state():
                    door_light.turn_off(write_to_database, settings, publisher)
                light_event.clear()
    except KeyboardInterrupt:
        print("Ending Door Light control")
    finally:
        if door_light:
            door_light.cleanup()
