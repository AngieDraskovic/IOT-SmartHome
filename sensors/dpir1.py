import time

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


class DPIR1:
    def __init__(self, pin, callback):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=lambda channel: callback(True))
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=lambda channel: callback(False))

    def cleanup(self):
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup()


def run_door_montion_sensor_loop(delay, sensor, stop_event):
    try:
        while not stop_event.is_set():
            time.sleep(delay)
    finally:
        sensor.cleanup()
