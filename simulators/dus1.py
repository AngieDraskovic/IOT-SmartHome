import random
import time

# DOOR ULTRASONIC SENSOR


def generate_values():
    while True:
        distance = random.uniform(0.5, 5.0)
        yield '{0:.3f}'.format(distance)


def run_dus1_simulator(delay, callback, stop_event, publish_event, settings):
    for distance in generate_values():
        time.sleep(delay)
        callback(distance, publish_event, settings)
        if stop_event.is_set():
            break


