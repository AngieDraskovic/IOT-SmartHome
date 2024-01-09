import threading
from simulators.DMS import run_DMS_simulator
from .utilites import Publisher

def DMS_callback(button, settings, publisher):
    temp_payload = {
        "measurement": "Key",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": button 
    }

    publisher.add_values(['Key'],[temp_payload])
    print("DMS: " + str(button) +  " pressed")


def run_DMS(settings, threads, stop_event):
    publisher = Publisher()
    if settings["simulated"]:
        print("starting DMS simulator")
        DMS_thread = threading.Thread(target = run_DMS_simulator, args=(2, DMS_callback, settings, publisher,stop_event))
        DMS_thread.start()
        threads.append(DMS_thread)
        print("DMS simulator started")
    else:
        from sensors.DMS import DMS
        print("Starting DMS loop")
        dms = DMS(settings['pins'])
        DMS_thread = threading.Thread(target=dms.run_loop, args=(stop_event, DMS_callback, settings, publisher))
        DMS_thread.start()
        threads.append(DMS_thread)