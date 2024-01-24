import json
import threading
import time
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT
import asyncio


class Alarm:

    def __init__(self):
        self.is_active = False
        self.is_triggered = False
        self.activated_sensors = set()  # Skup senzora koji su aktivirali alarm !
        self.system_active = False
        self.pin_code = "1234"  # Pretpostavljeni PIN kod
        self.code_entered = False   

    def activate_alarm(self, activation_sensor, delay=5, sleep = True):
        if self.system_active and sleep:
            time.sleep(delay)
        if self.is_active:
            return
        if self.code_entered == True:
            return
        self.activated_sensors.add(activation_sensor)
        self.is_active = True
        self.is_triggered = True
        alarm_message = {"Sensor": activation_sensor}
        print("activated: ", alarm_message)
        publish.single("ALARM ACTIVATION", json.dumps(alarm_message), hostname=HOSTNAME, port=PORT)
        publish.single("Alarm status", json.dumps({"system_active" : alarm.system_active, "active" : alarm.is_active}))

        self.send_message_to_front(activation_sensor)
        # i ovdje vjr treba aktivirati db i bb - Milosev dio, mozes to preko mqtt slati db i bb-u
        # milose mislim da ce tebi trebati ovaj delay od 10 sekundi za DMS,pa vrsi provjeru ako je activation sensor dms

    def activate_alarm_system(self):
        time.sleep(10)
        alarm.system_active = True
        

    def disable_alarm(self):
        self.code_entered = True
        time.sleep(10)
        self.code_entered = False


    def deactivate_alarm(self, deactivation_sensor, pin_input=""):
        print("test")
        if deactivation_sensor == "DMS" and pin_input == self.pin_code:  # ako ga DMS deaktivira ispraznim set aktivaionih senzora i gasim alarm definitvno
            self.is_active = False
            self.is_triggered = False
            self.system_active = False
            self.activated_sensors.clear()
            print("Alarm deaktiviran putem DMS-a sa ispravnim PIN-om")
            alarm_message = {"Sensor": deactivation_sensor}
            publish.single("ALARM DEACTIVATION", json.dumps(alarm_message), hostname=HOSTNAME, port=PORT)
            publish.single("Alarm status", json.dumps({"system_active" : alarm.system_active, "active" : alarm.is_active}))
            self.send_message_to_front(deactivation_sensor)
        elif deactivation_sensor in self.activated_sensors:  # ako su ga deaktirivirali DS1 ili DS2 gledam jesu li ga oba kako bih sigurno ugasila alarm
            print(f"pokusaj deaktivacije{deactivation_sensor}")
            self.activated_sensors.remove(deactivation_sensor)
            if not self.activated_sensors:
                self.is_active = False
                self.is_triggered = False
                alarm_message = {"Sensor": deactivation_sensor}
                print("deactivated: ", alarm_message)
                publish.single("ALARM DEACTIVATION", json.dumps(alarm_message), hostname=HOSTNAME, port=PORT)
                self.send_message_to_front(deactivation_sensor)

    def send_message_to_front(self, last_trigger):
        # last trigger mi cuva onoga koji ga je posljednji AKTIVIRAO a u slucaju deaktivacije ko ga je deaktivirao

        message_for_front = {"room": "ALARM", "state": self.is_active, "activated_by": list(self.activated_sensors),
                             "last_activated_by": last_trigger}

        publish.single("frontend/update", payload=json.dumps(message_for_front), hostname=HOSTNAME, port=PORT)


if __name__ == "__main__":
    alarm = Alarm()
    print("ALARM INITIATED")


    def on_message(client, userdata, message):
        decoded_message = message.payload.decode()
        data = json.loads(decoded_message)
        if message.topic == "home/alarm/activate":
            activation_sensor = next(iter(data))
            alarm_activation_thread = threading.Thread(target=alarm.activate_alarm, args=(activation_sensor,))
            alarm_activation_thread.start()
        
        elif message.topic == "home/alarm/deactivate":
            deactivation_sensor = next(iter(data))
            alarm.deactivate_alarm(deactivation_sensor, "")
        
        elif message.topic == "home/alarm/activate-system":
            if data["message"] == alarm.pin_code:
                alarm_activation_thread = threading.Thread(target=alarm.activate_alarm_system)
                alarm_activation_thread.start()
        
        elif message.topic == "home/alarm/deactivate-system":
            print("test")
            alarm.deactivate_alarm("DMS", data["message"])

        elif message.topic == "home/alarm/get_alarm_status":
            publish.single("Alarm status", json.dumps({"system_active" : alarm.system_active, "active" : alarm.is_active}))
        
        elif message.topic == "home/alarm/input_code":
            if data["message"] == alarm.pin_code:
                alarm_deactivation_thread = threading.Thread(target=alarm.disable_alarm)
                alarm_deactivation_thread.start()

        elif message.topic == "Motion":
            publish.single("get_people_num", 0)
        
        elif message.topic == "people_num":
            if data["message"] == 0:
                alarm.activate_alarm("RPIR")


    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message

    mqtt_client.connect(HOSTNAME, PORT)

    mqtt_client.subscribe("home/alarm/activate")
    mqtt_client.subscribe("home/alarm/deactivate")
    mqtt_client.subscribe("home/alarm/activate-system")
    mqtt_client.subscribe("home/alarm/get_alarm_status")
    mqtt_client.subscribe("home/alarm/input_code")
    mqtt_client.subscribe("home/alarm/deactivate-system")
    mqtt_client.subscribe("Motion")
    mqtt_client.subscribe("people_num")
    mqtt_client.loop_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("cao poz")
        mqtt_client.loop_stop()
