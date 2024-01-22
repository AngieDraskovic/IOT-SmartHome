import json
import time

import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT


class Alarm:

    def __init__(self):
        self.is_active = False
        self.is_triggered = False
        self.activated_sensors = set()  # Skup senzora koji su aktivirali alarm !
        self.pin_code = "1234"  # Pretpostavljeni PIN kod

    def activate_alarm(self, activation_sensor, delay=10):
        print(f"ALARM ACTIVATED BY {activation_sensor}")
        self.activated_sensors.add(activation_sensor)
        self.is_active = True
        self.is_triggered = True
        # ovdje cu vjr slati topic na server da bi i ovo upisao u bazu :)
        # i ovdje vjr treba aktivirati db i bb - Milosev dio, mozes to preko mqtt slati db i bb-u
        # milose mislim da ce tebi trebati ovaj delay od 10 sekundi za DMS, pa vrsi provjeru ako je activation sensor dms

    def deactivate_alarm(self, deactivation_sensor, pin_input=""):
        # ako ga DMS deaktivira ispraznim set aktivaionih senzora i gasim alarm definitvno
        if deactivation_sensor == "DMS" and pin_input == self.pin_code:
            self.is_active = False
            self.is_triggered = False
            self.activated_sensors.clear()
            print("Alarm deaktiviran putem DMS-a sa ispravnim PIN-om")
        # ako su ga deaktirivirali DS1 ili DS2 gledam jesu li ga oba kako bih sigurno ugasila alarm
        elif deactivation_sensor in self.activated_sensors:
            print(f"pokusaj deaktivacije{deactivation_sensor}")
            self.activated_sensors.remove(deactivation_sensor)
            if not self.activated_sensors:
                self.is_active = False
                self.is_triggered = False
                print("ALARM DEACTIVATED")


if __name__ == "__main__":
    alarm = Alarm()
    print("ALARM INITIATED")

    def on_message(client, userdata, message):
        if message.topic == "home/alarm/activate":
            decoded_message = message.payload.decode()
            activation_data = json.loads(decoded_message)
            activation_sensor = next(iter(activation_data))
            alarm.activate_alarm(activation_sensor)
        elif message.topic == "home/alarm/deactivate":
            print("Poruka primljena za deakt:", message.payload.decode())
            decoded_message = message.payload.decode()
            deactivation_data = json.loads(decoded_message)
            deactivation_sensor = next(iter(deactivation_data))
            alarm.deactivate_alarm(deactivation_sensor, "")

    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message

    mqtt_client.connect(HOSTNAME, PORT)

    mqtt_client.subscribe("home/alarm/activate")
    mqtt_client.subscribe("home/alarm/deactivate")
    mqtt_client.loop_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("cao poz")
        mqtt_client.loop_stop()
