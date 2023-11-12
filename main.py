import threading
from settings import load_settings
from components.ds1 import run_door_sensor_simulator
from components.dus1 import run_door_ultrasonic_simulator
from components.dl import handle_door_light, handle_commands
from components.dpir1 import run_door_motion_sensor_simulator
import time

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

if __name__ == "__main__":
    print('WELCOME TO YOUR SMART HOME....')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()

    try:
        ds1_settings = settings['DS1']
        run_door_sensor_simulator(ds1_settings, threads, stop_event)

        dus1_settings = settings['DUS1']
        run_door_ultrasonic_simulator(dus1_settings, threads, stop_event)

        dpir1_settings = settings['DPIR1']
        run_door_motion_sensor_simulator(dpir1_settings, threads, stop_event)

        door_light_thread = threading.Thread(target=handle_door_light)
        door_light_thread.start()
        threads.append(door_light_thread)

        command_thread = threading.Thread(target=handle_commands)
        command_thread.start()
        threads.append(command_thread)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        stop_event.set()
        for t in threads:
            t.join()