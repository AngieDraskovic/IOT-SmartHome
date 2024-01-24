import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT

mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, PORT)
mqtt_client.subscribe("activate/alarm_clock")
mqtt_client.subscribe("deactivate/buzzer")
mqtt_client.loop_start()


def on_message(client, userdata, message):
    if message.topic == "deactivate/buzzer":
        constant = True
    elif message.topic == "activate/alarm_clock":
        constant = False

constant = True

def run_b4sd(settings, stop_event):
    global constant
    while not stop_event.is_set():
        if settings['simulated']:
            from actuators.b4sd import display_simulator
            display_simulator(settings, constant)
        else:
            from actuators.b4sd import display
            display(settings, constant)
