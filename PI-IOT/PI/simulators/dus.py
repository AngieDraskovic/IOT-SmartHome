import random
import time

# DOOR ULTRASONIC SENSOR


import random


def generate_values():
    distance = 2.5
    approaching = True  # akoo se objekat priblizavaa

    while True:
        if approaching:
            distance -= random.uniform(0.1, 0.5)
            if distance <= 0.2:
                approaching = False
        else:
            distance += random.uniform(0.1, 0.5)
            if distance >= 2.5:
                approaching = True

        yield '{0:.3f}'.format(distance)


def run_dus_simulator(delay, callback, stop_event, publish_event, settings):
    for distance in generate_values():
        time.sleep(delay)
        callback(distance, publish_event, settings)
        if stop_event.is_set():
            break
