import threading

print_lock = threading.Lock()
light_event = threading.Event()
buzzer_event = threading.Event()
door_light_state = False


def handle_commands():
    try:
        print("Handling lights: x \nHandling buzzer: y\n>>")
        while True:
            command = input()
            if command == "x" or command == "X":
                light_event.set()
            elif command == "y" or command == "Y":
                buzzer_event.set()
    except KeyboardInterrupt:
        print("Ending command control")
