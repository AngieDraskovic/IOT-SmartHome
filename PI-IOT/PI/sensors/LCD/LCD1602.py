#!/usr/bin/env python3

import json
from sensors.LCD.PCF8574 import PCF8574_GPIO
from sensors.LCD.Adafruit_LCD1602 import Adafruit_CharLCD
from broker_settings import HOSTNAME, PORT
from time import sleep, strftime
from datetime import datetime

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

class LCD1602:
    def __init__(self, settings) -> None:
        self.settings = settings
        self.PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        self.PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
        # Create PCF8574 GPIO adapter.
        try:
            self.mcp = PCF8574_GPIO(self.PCF8574_address)
        except:
            try:
                self.mcp = PCF8574_GPIO(self.PCF8574A_address)
            except:
                print ('I2C Address Error !')
                exit(1)
        # Create LCD, passing in MCP GPIO adapter.
        self.lcd = Adafruit_CharLCD(pin_rs=settings["pin_rs"], pin_e=settings["pin_e"], pins_db=settings["pins_db"], GPIO=self.mcp)
        self.start_mqtt()
        
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe("Humidity")
        client.subscribe("Temperature")
        


    def display_information(self, client, userdata, message):  
        data = json.loads(message.payload.decode('utf-8'))
        if data["measurement"] == "Humidity":
            self.lcd.message( "Humidity " + str(data["value"]) )   # display the time
        else:
            self.lcd.message( 'Temperature: ' + str(data["value"]) +'\n' )# display CPU temperature


    def start_mqtt(self, ):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("localhost", 1883, 60)
        self.mqtt_client.loop_start()
        
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.display_information
    



    def get_cpu_temp(self, ):     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
        tmp = open('/sys/class/thermal/thermal_zone0/temp')
        cpu = tmp.read()
        tmp.close()
        return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
    
    def get_time_now(self, ):     # get system time
        return datetime.now().strftime('    %H:%M:%S')
        
    def loop(self, ):
        self.mcp.output(3,1)     # turn on LCD backlight
        self.lcd.begin(16,2)     # set number of LCD lines and columns
        self.start_mqtt()
            
    def destroy(self, ):
        self.lcd.clear()


