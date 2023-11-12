import random
import time

# DOOR MOTION SENSOR


def generate_values():
    while True:
        motion_detected = random.random() < 0.2   # 20% da se desio motion
        yield motion_detected


def run_dpir1_simulator(delay, callback, stop_event):
    for motion in generate_values():
        time.sleep(delay)
        callback(motion)
        if stop_event.is_set():
            break


