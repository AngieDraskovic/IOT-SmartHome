import threading
from simulators.ds1 import run_ds_simulator
from components.utilites import print_lock

# DOOR SENSOR


def door_sensor_callback(status):
    with print_lock:
        print(f"Door Status by DS1: {status}")


def run_door_sensor_simulator(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DS simulator")
        ds_thread = threading.Thread(target=run_ds_simulator, args=(1, door_sensor_callback, stop_event))
        ds_thread.start()
        threads.append(ds_thread)


