try:
    import RPi.GPIO as GPIO
except:
    pass
import time

class RPIR:
    def __init__(self, pin, number):
        self.pin = pin
        self.number = number
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=self.motion_detected)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.no_motion)

    def motion_detected(self):
        print("RPIR " + str(self.number)  + ": Motion detected")

    def no_motion(self):
        print("RPIR " + str(self.number)  + ": no longer detects movement")

    def cleanup(self):
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup(self.pin)

    def run_loop(self, delay, stop_event):
        try:
            while not stop_event:
                time.sleep(delay)
        finally:
            self.cleanup()