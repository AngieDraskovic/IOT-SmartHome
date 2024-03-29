import threading
import time
from components.RPIR import run_RPIR
from components.DHT import run_DHT
from components.ds import run_door_sensor_simulator
from components.dpir import run_door_motion_sensor_simulator
from components.dus import run_door_ultrasonic_simulator
from components.utilites import handle_commands
from components.gyro import run_gyro
from components.LCD import run_LCD
from settings import load_settings
from .components.utilites import Publisher


try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

if __name__ == "__main__":
    print('PI 2 STARTED')
    settings = load_settings('settingsPI2.json')
    threads = []
    stop_event = threading.Event()


    try:
        ds2_settings = settings['DS2']
        run_door_sensor_simulator(ds2_settings, threads, stop_event)

        dus2_settings = settings['DUS2']
        run_door_ultrasonic_simulator(dus2_settings, threads, stop_event)

        dpir2_settings = settings['DPIR2']
        run_door_motion_sensor_simulator(dpir2_settings, threads, stop_event)

        gsg_settings = settings["GSG"]
        run_gyro(gsg_settings, threads, stop_event)

        GLCD_settings = settings["GLCD"]
        run_LCD(GLCD_settings, threads, stop_event)
        #
        RDHT3_settings = settings['RDHT3']
        run_DHT(RDHT3_settings, threads, stop_event, 3)

        GDHT_settings = settings['GDHT']
        run_DHT(GDHT_settings, threads, stop_event, 5)  # 5 jer je peta vrta DHT-a

        rpirPublisher = Publisher()
        RPIR3_settings = settings['RPIR3']
        run_RPIR(RPIR3_settings, threads, stop_event, 3, rpirPublisher)

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