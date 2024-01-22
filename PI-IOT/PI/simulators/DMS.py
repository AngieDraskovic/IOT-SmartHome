import random
import time


def generate_values():
    buttons = ["1","2","3","A","4","5","6","B","7","8","9","C","*","0","#","#"]
    while True:
        button_id = random.randint(0,15)
        yield buttons[button_id] 

def run_DMS_simulator(delay, callback, settings, publisher, stop_event):
    for button in generate_values():
        time.sleep(delay)
        callback(button, settings, publisher)
        if stop_event.is_set():
            break