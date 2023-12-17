import time
import random

def generate_values():
    while True:
        pressed = random.randint(0,1)
        yield pressed 

def run_DB_simulator(delay, callback, stop_event):
    for pressed in generate_values():
        time.sleep(delay)
        callback(pressed)
        if stop_event.is_set():
            break