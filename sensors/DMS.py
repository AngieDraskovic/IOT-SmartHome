try:
    import RPi.GPIO as GPIO
except:
    pass
import time

class DMS:
    def __init__(self, pins):
        self.R1 = pins["R1"]
        self.R2 = pins["R2"]
        self.R3 = pins["R3"]
        self.R4 = pins["R4"]
        self.C1 = pins["C1"]
        self.C2 = pins["C2"]
        self.C3 = pins["C3"]
        self.C4 = pins["C4"]
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.R1, GPIO.OUT)
        GPIO.setup(self.R2, GPIO.OUT)
        GPIO.setup(self.R3, GPIO.OUT)
        GPIO.setup(self.R4, GPIO.OUT)

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



    def readLine(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(self.C1) == 1):
            print(characters[0])
        if(GPIO.input(self.C2) == 1):
            print(characters[1])
        if(GPIO.input(self.C3) == 1):
            print(characters[2])
        if(GPIO.input(self.C4) == 1):
            print(characters[3])
        GPIO.output(line, GPIO.LOW)

    def run_loop(self, stop_event):
        while not stop_event:
            self.readLine(self.R1, ["1","2","3","A"])
            self.readLine(self.R2, ["4","5","6","B"])
            self.readLine(self.R3, ["7","8","9","C"])
            self.readLine(self.R4, ["*","0","#","D"])
            time.sleep(0.2)

    
        