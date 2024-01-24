import time

try:
    import RPi.GPIO as GPIO
except:
    pass


class DB:
    def __init__(self, pin):
        self.pin = pin
        self.state = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.options = {False: self.turn_on, True: self.turn_off}

    def turn_on(self):
        pitch = 440
        duration = 1
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles):
            GPIO.output(self.pin, True)
            time.sleep(delay)
            GPIO.output(self.pin, False)
            time.sleep(delay)

    def turn_off(self):
        # self.Buzz.stop()
        pass

    
    def signal(self, write_to_database, settings, publisher, state):
        self.state = state
        self.options[self.state]()
        write_to_database(self.state, settings, publisher)

    def cleanup(self):
        GPIO.cleanup(self.pin)