import threading
import time
from simulators.RPIR import run_RPIR_simulator
from sensors.RPIR import RPIR
from components.utilites import print_lock


def RPIR_callback(rand_number, number):
    if rand_number == 1:
        with print_lock:
            print("RPIR " + str(number) + ": Motion detected")


def run_RPIR(settings, threads, stop_event, number):
    if settings["simulated"]:
        print("starting RPIR" + str(number) + " simulator")
        RPIR_thread = threading.Thread(target=run_RPIR_simulator, args=(2, RPIR_callback, stop_event, number))
        RPIR_thread.start()
        threads.append(RPIR_thread)
        print("RPIR simulator started")
    else:
        rpir = RPIR(settings["pin"], number)
        print("String RPIR" + str(number) + " loop")
        RPIR_thread = threading.Thread(target=rpir.run_loop, args=(2, stop_event))
        RPIR_thread.start()
        threads.append(RPIR_thread)
