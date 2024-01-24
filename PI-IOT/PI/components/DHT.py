import threading

from .utilites import Publisher
from simulators.DHT import run_DHT_simulator


def DHT_callback(humidity, temperature, code, number, settings, publisher):
    temp_payload = {
        "measurement": "Temperature",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": temperature,
        "id": number
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": humidity,
        "id": number
    }

    publisher.add_values(['Temperature', 'Humidity'], [temp_payload, humidity_payload])
    print("DHT" + str(number) + ">> Humidity: " + str(humidity) + ", Temperature: " + str(temperature))


def run_DHT(settings, threads, stop_event, number):
    publisher = Publisher()
    if settings['simulated']:
        print(f" {settings['name']} sumilator")
        dht1_thread = threading.Thread(target=run_DHT_simulator,
                                       args=(2, DHT_callback, stop_event, number, settings, publisher))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(f" {settings['name']} sumilator started")
    else:
        from sensors.DHT import run_dht_loop, DHT
        print(f"Starting  {settings['name']} loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop,
                                       args=(dht, 2, DHT_callback, stop_event, number, settings, publisher))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(f" {settings['name']} loop started")
