import threading
import time


door_light_event = threading.Event()
door_light_state = False


class DL:
    def __init__(self):
        self.on = False



def handle_door_light():
    global door_light_state
    try:
        while True:
            if door_light_state:
                print("Door Light is ON")
            else:
                print("Door Light is OFF")
            time.sleep(1)  # za smanjivanje frekvencije ispisa :)
    except KeyboardInterrupt:
        print("Ending Door Light control")


def handle_commands():
    global door_light_state
    try:
        print("Enter '1' to turn ON the light, '2' to turn OFF: ")
        while True:
            command = input()
            if command == "1":
                door_light_state = True
            elif command == "2":
                door_light_state = False
    except KeyboardInterrupt:
        print("Ending command control")
