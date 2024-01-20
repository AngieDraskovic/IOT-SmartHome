import json
import threading

import paho.mqtt.publish as publish

from broker_settings import HOSTNAME, PORT

print_lock = threading.Lock()
# light_event = threading.Event()
buzzer_event = threading.Event()
door_light_state = False


def handle_commands():
    print("Handling lights: x \nHandling buzzer: y\n>>")
    while True:
        command = input()
        # if command == "x" or command == "X":
        #     light_event.set()
        if command == "y" or command == "Y":
            buzzer_event.set()


class Publisher:
    def __init__(self) -> None:
        self.dht_batch = []
        self.publish_data_counter = 0
        self.publish_data_limit = 1
        self.counter_lock = threading.Lock()
        self.publish_event = threading.Event()
        self.publisher_thread = threading.Thread(target=self.publisher_task)
        self.publisher_thread.daemon = True
        self.publisher_thread.start()

    def publisher_task(self):
        while True:
            self.publish_event.wait()
            with self.counter_lock:
                local_dht_batch = self.dht_batch.copy()
                device_names = set(json.loads(item[1])['name'] for item in local_dht_batch)
                self.publish_data_counter = 0
                self.dht_batch.clear()
            publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
            print(f'published {self.publish_data_limit} for {device_names}')
            self.publish_event.clear()

    def add_values(self, labels, values):
        with self.counter_lock:
            for index, label in enumerate(labels):
                self.dht_batch.append((label, json.dumps(values[index]), 0, True))
            self.publish_data_counter += 1
        if self.publish_data_counter >= self.publish_data_limit:
            self.publish_event.set()
