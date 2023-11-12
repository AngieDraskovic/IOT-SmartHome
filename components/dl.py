from components.utilites import *


def handle_door_light(settings):
    global door_light_state
    door_light = None
    if not settings['simulated']:
        from actuators.dl import DL
        door_light = DL(settings['pin'])
    try:
        while True:
            if settings['simulated']:
                light_event.wait()
                door_light_state = not door_light_state
                state_str = "ON" if door_light_state else "OFF"
                print(f"Door Light turned {state_str}")
                light_event.clear()
            else:
                light_event.wait()
                if door_light and not door_light.get_state():
                    door_light.turn_on()
                elif door_light and door_light.get_state():
                    door_light.turn_off()
                light_event.clear()
    except KeyboardInterrupt:
        print("Ending Door Light control")
    finally:
        if door_light:
            door_light.cleanup()
