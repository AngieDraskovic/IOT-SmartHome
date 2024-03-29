import time

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


class DS:
    def __init__(self, pin, publish_event, callback, settings):
        self.pin = pin
        self.publish_event = publish_event
        self.callback = callback
        self.settings = settings
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=lambda channel: callback(GPIO.input(pin) == GPIO.HIGH),
                              bouncetime=100)

    def cleanup(self):
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup(self.pin)

    def motion_detected(self):
        if(GPIO.input(self.pin) == GPIO.HIGH):
            self.callback("open", self.publish_event, self.settings)
        else:
            self.callback("closed", self.publish_event, self.settings)


def run_door_sensor_loop(delay, sensor, stop_event, publish_event, settings):
    try:
        while not stop_event.is_set():
            time.sleep(delay)
    finally:
        sensor.cleanup()
