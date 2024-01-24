
def run_b4sd(settings, stop_event):
    while not stop_event.is_set():
        if settings['simulated']:
            from actuators.b4sd import display_simulator
            display_simulator(settings)
        else:
            from actuators.b4sd import display
            display(settings)
