
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

    def turn_on(self):
        if not self.state:
            GPIO.output(self.pin, GPIO.HIGH)
            self.state = True
            print("Door Light turned ON")

    def turn_off(self):
        if self.state:
            GPIO.output(self.pin, GPIO.LOW)
            self.state = False
            print("Door Light turned OFF")

    def get_state(self):
        return self.state

    def cleanup(self):
        GPIO.cleanup(self.pin)
