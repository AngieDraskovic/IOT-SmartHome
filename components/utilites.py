import threading

print_lock = threading.Lock()
light_event = threading.Event()
door_light_state = False


def handle_commands():
    try:
        print("Click on 'x' for handling DOOR LIGHT: ")
        while True:
            command = input()
            if command == "x" or command == "X":
                light_event.set()
    except KeyboardInterrupt:
        print("Ending command control")
