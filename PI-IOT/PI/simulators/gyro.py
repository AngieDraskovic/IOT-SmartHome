import random
import time


def generate_values():
    while True:
        values = []
        for i in range(6):
            values.append(random.randint(0,1000)/20000)
        yield values

def run_gyro_simulator(delay, callback, stop_event, settings, publisher):
    for values in generate_values():
        time.sleep(delay)
        callback(values, settings, publisher)
        if stop_event.is_set():
            break