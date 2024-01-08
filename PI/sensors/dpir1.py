import time

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


class DPIR1:
    def __init__(self, pin, publish_event, callback, settings):
        self.pin = pin
        self.publish_event = publish_event
        self.callback = callback
        self.settings = settings
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=self.motion_detected)
        # GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.no_motion)

    def cleanup(self):
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup()


    def motion_detected(self, x):
        self.callback(True, self.publish_event, self.settings)

    def no_motion(self):
        self.callback(False, self.publish_event, self.settings)

def run_door_montion_sensor_loop(delay, sensor, stop_event):
    try:
        while not stop_event.is_set():
            time.sleep(delay)
    finally:
        # sensor.cleanup()
        pass