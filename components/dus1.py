import threading
from simulators.dus1 import run_dus1_simulator
from components.utilites import print_lock

# DOOR ULTRASONIC SENSOR


def dus1_callback(distance):
    with print_lock:
        print(f"Distance measured by DUS1: {distance} meters")


def run_door_ultrasonic_simulator(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DUS1 simulator")
        dus1_thread = threading.Thread(target=run_dus1_simulator, args=(5, dus1_callback, stop_event))
        dus1_thread.start()
        threads.append(dus1_thread)
    else:
        from sensors.dus1 import run_ultrasonic_sensor_loop, DUS1
        print("Starting DUS1 loop")
        dus1 = DUS1(settings['pin_trig'], settings['pin_echo'])
        dus1_thread = threading.Thread(target=run_ultrasonic_sensor_loop, args=(5, dus1, dus1_callback, stop_event))
        dus1_thread.start()
        threads.append(dus1_thread)
