import time
import enum

from apps import App
from buttons import Buttons
from display import Display


class BabyState(enum.Enum):
    awake = 0
    asleep = 1


class BabyTimer:
    # BabyTimer has 2 states - AWAKE and ASLEEP, and once started,
    # it adds time to whichever timer is active.
    # Pressing button A will note the time and switch states, starting to count
    # for the next state.
    # Pressing button B will reset both counters to zero
    def __init__(self, scheduler):
        App.__init__(self, "Baby Timer", "babytimer")
        self.display = Display(scheduler)
        self.scheduler = scheduler
        self.buttons = Buttons()

        self.switcher = {
            BabyState.awake: "*",
            BabyState.asleep: "-"
        }
        self.state = BabyState.awake
        self.total_duration = {
            BabyState.awake: 0,
            BabyState.asleep: 0
        }
        self.last_reset_time = None

        self.enabled = False
        self.started = False

        # Callback that drives update
        scheduler.schedule("time-second", 1000, self.time_increment_callback)
        self.buttons.add_callback(2, self.start_callback, max=500)
        self.buttons.add_callback(3, self.stop_callback, max=500)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        self.started = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False

    # This simply updates the display
    def time_increment_callback(self, t):
        if self.enabled and self.started:
            self.update_display()

    # Runs when the start button is pressed
    def start_callback(self):
        # If not enabled, don't do anything
        if not self.enabled:
            return None

        # Log time and switch state if already running
        if self.started:
            self.total_duration[self.state] += _elapsed_time()
            self.state = _next_state()

        # Mark as started
        self.started = True
        self.last_reset_time = time.time()

    def stop_callback(self):
        self.started = False

    def _elapsed_time(self):
        return self.time() - self.last_reset_time

    # Display current state and time
    def update_display(self):
        t = self.state_string() + "%02d:%02d" % (self.current_duration //
                                                 3600, (self.current_duration/60) % 60)
        self.display.show_text(t)

    def state_string(self):
        return self.switcher.get(self.state)
