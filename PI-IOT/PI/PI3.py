import threading
import time
from components.RPIR import run_RPIR
from components.DHT import run_DHT
from components.bir import run_bir
from components.b4sd import run_b4sd
from components.brgb import run_brgb
from components.utilites import handle_commands
from settings import load_settings

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

if __name__ == "__main__":
    print('PI 3 STARTED')
    settings = load_settings('settingsPI3.json')
    threads = []
    stop_event = threading.Event()

    try:
        # RPIR4_settings = settings['RPIR4']
        # run_RPIR(RPIR4_settings, threads, stop_event, 3)
        #
        # RDHT4_settings = settings['RDHT4']
        # run_DHT(RDHT4_settings, threads, stop_event, 4)
        #
        BIR_settings = settings['BIR']
        run_bir(BIR_settings, threads, stop_event)

        BRGB_settings = settings['BRGB']
        brgb_thread = threading.Thread(target=run_brgb, args=(BRGB_settings,stop_event))
        brgb_thread.start()
        threads.append(brgb_thread)

        b4sd_settings = settings['B4SD']
        b4sd_thread = threading.Thread(target=run_b4sd, args=(b4sd_settings, stop_event))
        b4sd_thread.start()
        threads.append(b4sd_thread)

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