import random
import time

# DOOR SENSOR


def generate_values():
    while True:
        door_status = random.choice(["open", "closed"])
        yield door_status


def run_ds_simulator(delay, callback, stop_event):
    for door_status in generate_values():
        time.sleep(delay)
        callback(door_status)
        if stop_event.is_set():
            break


