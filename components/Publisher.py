import threading
import paho.mqtt.publish as publish
import json
from components.broker_settings import HOSTNAME,PORT


class Publisher:
    def __init__(self) -> None:    
        self.dht_batch = []
        self.publish_data_counter = 0
        self.publish_data_limit = 5
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
                self.publish_data_counter = 0
                self.dht_batch.clear()
            publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
            print(f'published {self.publish_data_limit} dht values')
            self.publish_event.clear()

    def add_values(self, labels, values):
        with self.counter_lock:
            for index,label in enumerate(labels):
                self.dht_batch.append((label, json.dumps(values[index]), 0, True))
            self.publish_data_counter += 1
        if self.publish_data_counter >= self.publish_data_limit:
            self.publish_event.set()