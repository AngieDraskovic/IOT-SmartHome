import threading
import time
from simulators.RDHT import run_RDHT_simulator

def RDHT_callback(humidity, temperature, number):
    print("Number: " + str(number) + ", Humidity: " + str(humidity) + ", Temperature: " + str(temperature))

def run_RDHT(settings, threads, stop_event, number):
        if settings['simulated']:
            print("Starting RDHT" + str(number) + " sumilator")
            dht1_thread = threading.Thread(target = run_RDHT_simulator, args=(2, RDHT_callback, stop_event, number))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht1 sumilator started")
        else:
            pass