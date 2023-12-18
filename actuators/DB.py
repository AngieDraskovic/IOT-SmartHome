try:
    import RPi.GPIO as GPIO
except:
    pass

class DB:
    def __init__(self, pin):
        self.pin = pin
        self.state = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.Buzz = GPIO.PWM(pin, 440)
        self.options = {False: self.turn_on, True: self.turn_off}

    def turn_on(self):
        self.Buzz.start(50)

    def turn_off(self):
        self.Buzz.stop()

    def signal(self, write_to_database, settings, publisher):
        self.State = not self.State
        self.options[self.State]()
        write_to_database(not self.State, settings, publisher)

    def cleanup(self):
        GPIO.cleanup(self.pin)