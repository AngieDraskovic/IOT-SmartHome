import time

from components.utilites import print_lock

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


class DUS:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(trig_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)

    def get_distance(self, TRIG_PIN, ECHO_PIN):
        GPIO.output(TRIG_PIN, False)
        time.sleep(0.2)
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        max_iter = 100

        iter = 0
        while GPIO.input(ECHO_PIN) == 0:
            if iter > max_iter:
                return None
            pulse_start_time = time.time()
            iter += 1

        iter = 0
        while GPIO.input(ECHO_PIN) == 1:
            if iter > max_iter:
                return None
            pulse_end_time = time.time()
            iter += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300) / 2
        return distance

    def cleanup(self):
        GPIO.cleanup()


def run_ultrasonic_sensor_loop(delay, sensor, callback, stop_event, publish_event, settings):
    try:
        while not stop_event.is_set():
            distance = sensor.get_distance()
            if distance is not None:
                callback(distance, publish_event, settings)
            else:
                with print_lock:
                    print(f"Measurement by {settings['name']} timed out")
            time.sleep(delay)
    finally:
        sensor.cleanup()
