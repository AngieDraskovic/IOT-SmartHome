import time
import random

def generate_values():
    while True:
        rand_number = random.randint(0,2)
        yield rand_number

def run_RPIR_simulator(delay, callback, stop_event, number, settings, publisher):
    for rand_number in generate_values():
        time.sleep(delay)
        callback(rand_number, number, settings, publisher)
        if stop_event.is_set():
            break