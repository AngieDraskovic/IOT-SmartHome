import threading

from .utilites import Publisher
from simulators.DMS import run_DMS_simulator


def DMS_callback(button, settings, publisher):
    temp_payload = {
        "measurement": "Key",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": button
    }

    publisher.add_values(['Key'], [temp_payload])
    print("DMS: " + str(button) + " pressed")


def run_DMS(settings, threads, stop_event):
    publisher = Publisher(publish_data_limit=1)
    if settings["simulated"]:
        print(f"starting {settings['name']} simulator")
        DMS_thread = threading.Thread(target=run_DMS_simulator, args=(2, DMS_callback, settings, publisher, stop_event))
        DMS_thread.start()
        threads.append(DMS_thread)
        print(f"{settings['name']} simulator started")
    else:
        from ..sensors.DMS import DMS
        print(f"Starting {settings['name']} loop")
        dms = DMS(settings['pins'])
        DMS_thread = threading.Thread(target=dms.run_loop, args=(stop_event, DMS_callback, settings, publisher))
        DMS_thread.start()
        threads.append(DMS_thread)
