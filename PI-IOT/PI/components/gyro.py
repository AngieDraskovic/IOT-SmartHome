import threading

from .utilites import Publisher
from simulators.gyro import run_gyro_simulator
# from sensors.Gyro.MPU6050 import MPU6050


def gyro_callback(values, settings, publisher):
    distance = abs(values[0] * 9.81) + abs(values[1] * 9.81)
    payload = {
        "measurement": "gyro",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "Gx": values[0], 
        "Gy": values[1], 
        "Gz": values[2], 
        "Ax": values[3], 
        "Ay": values[4], 
        "Az": values[5], 
        "distance" : distance,
        "id": 1
    }

    print("GSG: distance travelled: " + str(distance))
    publisher.add_values(['gyro'],[payload])
            

def run_gyro(settings, threads, stop_event):
    publisher = Publisher()
    if settings["simulated"]:
        print("starting GSG simulator")
        gyro_thread = threading.Thread(target = run_gyro_simulator, args=(1, gyro_callback, stop_event, settings, publisher))
        gyro_thread.start()
        threads.append(gyro_thread)
        print("gyro simulator started")
    else:
        # gyro = MPU6050(settings = settings, publisher = publisher)
        # gyro.dmp_initialize()
        # print("Starting gsg loop")
        # gyro_thread = threading.Thread(target=gyro.run_loop, args=(gyro_callback, stop_event))
        # gyro_thread.start()
        # threads.append(gyro_thread)
        pass
