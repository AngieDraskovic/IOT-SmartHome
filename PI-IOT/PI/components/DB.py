import time
from actuators import DB
from .utilites import buzzer_event, Publisher
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT



mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, PORT)
mqtt_client.subscribe("activate/buzzer")
mqtt_client.subscribe("activate/alarm_clock")
mqtt_client.subscribe("deactivate/buzzer")
mqtt_client.loop_start()

device_name = "DB"


def on_message(client, userdata, message):
    if message.topic == "activate/buzzer":
        buzzer_event.set()
    elif message.topic == "deactivate/buzzer":
        buzzer_event.clear()
    elif message.topic == "activate/alarm_clock" and device_name == "BB":
        buzzer_event.set()

mqtt_client.on_message = on_message

def write_to_database(on, settings, publisher):
    payload = {
        "measurement": "DoorBuzzer",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": on, 
    }
    publisher.add_values(['DoorBuzzer'],[payload])



def run_DB(settings, name, stop_event):
    global device_name
    device_name = name
    buzzer_on = False
    db = None
    buzzer = {False: "OFF", True: "ON"}
    if not settings["simulated"]:
        db = DB(settings["pin"])
    publisher = Publisher()
    print(settings["simulated"])
    while not stop_event.is_set():
        if settings["simulated"]:
            buzzer_event.wait()
            buzzer_on = True
            while buzzer_event.is_set():
                write_to_database(buzzer_on, settings, publisher)
                print(device_name + " is now: " + buzzer[buzzer_on])
                time.sleep(1)
            buzzer_on = False
            print(device_name + " is now: " + buzzer[buzzer_on])
        else:
            buzzer_event.wait()
            while buzzer_event.is_set():
                db.signal(write_to_database, settings, publisher, False)
            
            db.signal(write_to_database, settings, publisher, True)
