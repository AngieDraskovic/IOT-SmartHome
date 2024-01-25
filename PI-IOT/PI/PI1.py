import threading
import time

from components.DB import run_DB
from components.DMS import run_DMS
from components.DHT import run_DHT
from components.RPIR import run_RPIR
from components.dl import handle_door_light
from components.dpir import run_door_motion_sensor_simulator
from components.ds import run_door_sensor_simulator
from components.dus import run_door_ultrasonic_simulator
from components.utilites import handle_commands
from settings import load_settings
from .components.utilites import Publisher

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

if __name__ == "__main__":
    print('PI 1 STARTED')
    settings = load_settings('settingsPI1.json')
    threads = []
    stop_event = threading.Event()

    try:
        ds1_settings = settings['DS1']
        run_door_sensor_simulator(ds1_settings, threads, stop_event)

        dus1_settings = settings['DUS1']
        run_door_ultrasonic_simulator(dus1_settings, threads, stop_event)

        DB_settings = settings['DB']
        DB_thread = threading.Thread(target=run_DB, args=(DB_settings,"DB", stop_event))
        DB_thread.start()
        threads.append(DB_thread)


        DMS_settings = settings['DMS']
        run_DMS(DMS_settings, threads, stop_event)

        rpirPublisher = Publisher()
        RPIR1_settings = settings['RPIR1']
        run_RPIR(RPIR1_settings, threads, stop_event, 1, rpirPublisher)
        
        RPIR2_settings = settings['RPIR2']
        run_RPIR(RPIR2_settings, threads, stop_event, 2, rpirPublisher)
        
        rdhtPublisher = Publisher()
        RDHT1_settings = settings['RDHT1']
        run_DHT(RDHT1_settings, threads, stop_event, 1, rdhtPublisher)
        
        RDHT2_settings = settings['RDHT2']
        run_DHT(RDHT2_settings, threads, stop_event, 2, rdhtPublisher)

        dpir1_settings = settings['DPIR1']
        run_door_motion_sensor_simulator(dpir1_settings, threads, stop_event)

        dl_settings = settings['DL']
        door_light_thread = threading.Thread(target=handle_door_light, args=(dl_settings,))
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