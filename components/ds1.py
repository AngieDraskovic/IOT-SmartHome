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
        ds1_thread = threading.Thread(target=run_ds_simulator, args=(3, door_sensor_callback, stop_event))
        ds1_thread.start()
        threads.append(ds1_thread)
    else:
        from sensors.ds1 import run_door_sensor_loop, DS1
        print("Starting DS1 loop")
        ds1 = DS1(settings['pin'], door_sensor_callback)
        ds1_thread = threading.Thread(target=run_door_sensor_loop, args=(ds1, 3, stop_event))
        ds1_thread.start()
        threads.append(ds1_thread)
