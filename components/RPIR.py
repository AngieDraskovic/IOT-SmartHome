import threading
import time
from simulators.RPIR import run_RPIR_simulator
from sensors.RPIR import RPIR
from components.Publisher import Publisher

def RPIR_callback(rand_number, number, settings, publisher):
    payload = {
        "measurement": "Motion",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": True, 
        "id": number
    }
    if rand_number == 1:
        publisher.add_values(['Motion'],[payload])
        print("RPIR " + str(number)  + ": Motion detected")
    else:
        payload["value"] = False
        publisher.add_values(['Motion'],[payload])
        print("RPIR " + str(number)  + ": no longer detects movement")
            
def run_RPIR(settings, threads, stop_event, number):
    publisher = Publisher()
    if settings["simulated"]:
        print("starting RPIR" + str(number) + " simulator")
        RPIR_thread = threading.Thread(target = run_RPIR_simulator, args=(2, RPIR_callback, stop_event, number, settings, publisher))
        RPIR_thread.start()
        threads.append(RPIR_thread)
        print("RPIR simulator started")
    else:
        rpir = RPIR(settings["pin"], number, settings, publisher)
        print("String RPIR" + str(number) + " loop")
        RPIR_thread = threading.Thread(target = rpir.run_loop, args=(2, stop_event))
        RPIR_thread.start()
        threads.append(RPIR_thread)
