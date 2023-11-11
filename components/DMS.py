import threading
import time
from simulators.DMS import run_DMS_simulator

def DMS_callback(button_id):
    buttons = [1,2,3,"A",4,5,6,"B",7,8,9,"C","*",0,"#","#"]
    print(str(buttons[button_id]) +  " pressed")

def run_DMS(settings, threads, stop_event):
    if settings["simulated"]:
        print("starting DMS simulator")
        DMS_thread = threading.Thread(target = run_DMS_simulator, args=(2, DMS_callback, stop_event))
        DMS_thread.start()
        threads.append(DMS_thread)
        print("DMS simulator started")
    else:
        pass