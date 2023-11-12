import threading
import time


door_light_state = False


class DL:
    def __init__(self):
        self.on = False


light_on_event = threading.Event()
light_off_event = threading.Event()


def handle_door_light():
    global door_light_state
    try:
        while True:
            light_on_event.wait()
            door_light_state = True
            print("Door Light turned ON (DL)")
            light_on_event.clear()

            light_off_event.wait()
            door_light_state = False
            print("Door Light turned OFF (DL)")
            light_off_event.clear()
    except KeyboardInterrupt:
        print("Ending Door Light control")


def handle_commands():
    global door_light_state
    try:
        print("Enter '1' to turn ON the light, '2' to turn OFF: ")
        while True:
            command = input()
            if command == "1" and not door_light_state:
                light_on_event.set()
            elif command == "2" and door_light_state:
                light_off_event.set()
    except KeyboardInterrupt:
        print("Ending command control")
