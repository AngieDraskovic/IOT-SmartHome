
try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


class DL:
    def __init__(self, pin):
        self.pin = pin
        self.state = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    def turn_on(self, callback, settings, publisher):
        if not self.state:
            GPIO.output(self.pin, GPIO.HIGH)
            self.state = True
            callback(1, settings, publisher)
            print("Door Light turned ON")

    def turn_off(self, callback, settings, publisher):
        if self.state:
            GPIO.output(self.pin, GPIO.LOW)
            self.state = False
            callback(0, settings, publisher)
            print("Door Light turned OFF")

    def get_state(self):
        return self.state

    def cleanup(self):
        GPIO.cleanup(self.pin)
