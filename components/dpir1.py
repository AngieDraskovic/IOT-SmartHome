import threading
from simulators.dpir1 import run_dpir1_simulator
from components.utilites import print_lock

# DOOR MOTION SENSOR


def door_motion_callback(motion):
    if motion:
        with print_lock:
            print("Motion detected by DPIR1")

    else:
        with print_lock:
            print("Motion not detected by DPIR1")


def run_door_motion_sensor_simulator(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DPIR1 simulator")
        dpir1_thread = threading.Thread(target=run_dpir1_simulator, args=(2, door_motion_callback, stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
    else:
        from sensors.dpir1 import run_door_montion_sensor_loop, DPIR1
        print("Starting DPIR1 loop")
        dpir1 = DPIR1(settings['pin'], door_motion_callback)
        dpir1_thread = threading.Thread(target=run_door_montion_sensor_loop, args=(dpir1, 2, stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)


