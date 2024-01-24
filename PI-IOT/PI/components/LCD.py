import threading

from .utilites import Publisher
from sensors.LCD.LCD1602 import LCD1602
  

def run_LCD(settings, threads, stop_event):
    if not settings["simulated"]:
        lcd = LCD1602(settings)
        print("Starting LCD loop")
        LCD_thread = threading.Thread(target=lcd.start_mqtt)
        LCD_thread.start()
        threads.append(LCD_thread)
        pass
