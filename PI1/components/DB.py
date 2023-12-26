
from ..actuators.DB import DB
from .utilites import buzzer_event, Publisher


def write_to_database(on, settings, publisher):
    payload = {
        "measurement": "DoorBuzzer",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": on, 
    }
    publisher.add_values(['DoorBuzzer'],[payload])



def run_DB(settings):
    buzzer_on = False
    db = None
    buzzer = {False: "OFF", True: "ON"}
    if not settings["simulated"]:
        db = DB(settings["pin"])
    publisher = Publisher()
    while True:
        if settings["simulated"]:
            buzzer_event.wait()
            buzzer_on = not buzzer_on
            write_to_database(buzzer_on, settings, publisher)
            print("Buzzer is now: " + buzzer[buzzer_on])
            buzzer_event.clear()
        else:
            buzzer_event.wait()
            db.signal(write_to_database, settings, publisher)
            buzzer_event.clear()
