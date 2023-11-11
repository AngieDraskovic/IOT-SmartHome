import threading
import time
from simulators.DB import run_DB_simulator

def DB_callback(pressed):
    if pressed:
        print("Buzzer pressed")

def run_DB(settings, threads, stop_event):
    if settings["simulated"]:
        print("starting DB simulator")
        DB_thread = threading.Thread(target = run_DB_simulator, args=(2, DB_callback, stop_event))
        DB_thread.start()
        threads.append(DB_thread)
        print("DB simulator started")
    else:
        pass