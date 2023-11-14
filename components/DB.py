from components.utilites import *
from actuators.DB import *


def run_DB(settings):
    buzzer_on = False
    db = None
    buzzer = {False: "OFF", True: "ON"}
    if not settings["simulated"]:
        db = DB(settings["pin"])
    try:
        while True:
            if settings["simulated"]:
                buzzer_event.wait()
                buzzer_on = not buzzer_on
                print("Buzzer is now: " + buzzer[buzzer_on])
                buzzer_event.clear()
            else:
                buzzer_event.wait()
                db.signal()
                buzzer_event.clear()
    except KeyboardInterrupt:
        print("Ending Buzzer control")
    finally:
        if db:
            db.cleanup()
