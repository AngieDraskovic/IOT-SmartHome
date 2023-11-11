import time
import random

def generate_values():
    while True:
        button_id = random.randint(0,15)
        yield button_id 

def run_DMS_simulator(delay, callback, stop_event):
    for button_id in generate_values():
        time.sleep(delay)
        callback(button_id)
        if stop_event.is_set():
            break