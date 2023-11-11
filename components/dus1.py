import threading
from simulators.dus1 import run_dus1_simulator
from components.utilites import print_lock

# DOOR ULTRASONIC SENSOR


def dus1_callback(distance):
    with print_lock:
        print(f"Distance measured by DUS1: {distance} meters")


def run_door_ultrasonic_simulator(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DS simulator")
        ds_thread = threading.Thread(target=run_dus1_simulator, args=(2, dus1_callback, stop_event))
        ds_thread.start()
        threads.append(ds_thread)


