import time

from apps import App
from buttons import Buttons
from display import Display


class All(App):
    iconList = [
        "MoveOn",
        "AlarmOn",
        "CountDown",
        "°F",
        "°C",
        "AM",
        "PM",
        "CountUp",
        "Hourly",
        "AutoLight",
        "Mon",
        "Tue",
        "Wed",
        "Thur",
        "Fri",
        "Sat",
        "Sun",
    ]

    def __init__(self, scheduler, logger):
        App.__init__(self, scheduler, logger)
        self.enabled = False
        self.started = False
        self.buttons = Buttons()
        self.display = Display(scheduler)
        self.active = False

        # Callback that drives update
        scheduler.schedule("time-second", 5000, self.display_update_callback)

    def enable(self):
        self.enabled = True
        self.buttons.add_callback(2, self.start_callback, max=500)
        self.buttons.add_callback(3, self.stop_callback, max=500)

    def disable(self):
        self.enabled = False
        self.started = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False

    # This simply updates the display
    def display_update_callback(self, t):
        if self.enabled:
            self.update_display()

    # Runs when the start button is pressed
    def start_callback(self, t):
        self.started = True

    def stop_callback(self, t):
        print("Stop pressed")
        self.started = False

    def update_display(self):
        for i in range(0, 22, 3):
            self.display.show_char("all", i)

        for i in All.iconList:
            self.display.show_icon(i)
