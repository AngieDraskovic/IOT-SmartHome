try:
    import RPi.GPIO as GPIO
except:
    pass
import time

class RPIR:
    def __init__(self, pin, number, callback, settings, publisher):
        self.pin = pin
        self.number = number
        self.callback = callback
        self.settings = settings
        self.publisher = publisher
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=self.motion_detected)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.no_motion)

    def motion_detected(self):
        self.callback(1, self.number, self.settings, self.publisher)

    def no_motion(self):
        self.callback(0, self.number, self.settings, self.publisher)

    def cleanup(self):
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup(self.pin)

    def run_loop(self, delay, stop_event):
        try:
            while not stop_event:
                time.sleep(delay)
        finally:
            self.cleanup()