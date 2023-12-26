import threading
from PI1.simulators.RDHT import run_RDHT_simulator
from .utilites import Publisher

def RDHT_callback(humidity, temperature, code, number, settings, publisher):
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

    publisher.add_values(['Temperature', 'Humidity'],[temp_payload, humidity_payload])
    print("RDHT" + str(number) + ">> Humidity: " + str(humidity) + ", Temperature: " + str(temperature))

def run_RDHT(settings, threads, stop_event, number):
        publisher = Publisher()
        if settings['simulated']:
            print("Starting RDHT" + str(number) + " sumilator")
            dht1_thread = threading.Thread(target = run_RDHT_simulator, args=(2, RDHT_callback, stop_event, number, settings, publisher))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht1 sumilator started")
        else:
            from PI1.sensors.RDHT import run_dht_loop, RDHT
            print("Starting RDHT" + str(number) + " loop")
            dht = RDHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, RDHT_callback, stop_event, number, settings, publisher))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("RDHT" + str(number) + " loop started")