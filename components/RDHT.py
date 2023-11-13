import threading
import time
from simulators.RDHT import run_RDHT_simulator

def RDHT_callback(humidity, temperature, code, number):
    print("RDHT" + str(number) + ">> Humidity: " + str(humidity) + ", Temperature: " + str(temperature))

def run_RDHT(settings, threads, stop_event, number):
        if settings['simulated']:
            print("Starting RDHT" + str(number) + " sumilator")
            dht1_thread = threading.Thread(target = run_RDHT_simulator, args=(2, RDHT_callback, stop_event, number))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht1 sumilator started")
        else:
            from sensors.RDHT import run_dht_loop, RDHT
            print("Starting RDHT" + str(number) + " loop")
            dht = RDHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, RDHT_callback, stop_event, number))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("RDHT" + str(number) + " loop started")