import time

from apps import App
from buttons import Buttons
from display import Display


class BabyState:
    awake = 0
    asleep = 1


class BabyTimer(App):
    # BabyTimer has 2 states - AWAKE and ASLEEP, and once started,
    # it adds time to whichever timer is active.
    # Pressing button A will note the time and switch states, starting to count
    # for the next state.
    # Pressing button B will reset both counters to zero
    def __init__(self, scheduler, logger):
        App.__init__(self, "Baby Timer", "babytimer", logger)
        self.display = Display(scheduler)
        self.scheduler = scheduler
        self.buttons = Buttons()

        self.state_icons = {
            BabyState.awake: "CountUp",
            BabyState.asleep: "CountDown"
        }
        self.state = BabyState.awake
        self.total_duration = {
            BabyState.awake: 0,
            BabyState.asleep: 0
        }
        self.last_reset_time = time.time()
        self.last_displayed_text = ""
        self.last_displayed_state = None

        self.enabled = False
        self.started = False

        # Callback that drives update
        scheduler.schedule("time-second", 1000, self.update_display_callback)

    def enable(self):
        self.enabled = True
        self.buttons.add_callback(2, self.start_callback, max=500)
        # self.buttons.add_callback(3, self.stop_callback, max=500)

    def disable(self):
        self.enabled = False
        self.started = False
        self.buttons.remove_callback(2, self.start_callback, max=500)
        # self.buttons.remove_callback(3, self.stop_callback, max=500)

    def start(self):
        self.log("Timer Started")
        self.started = True

    def stop(self):
        self.log("Timer Stopped")
        self.started = False

    # This simply updates the display
    def update_display_callback(self, _t):
        if self.enabled:
            self.update_display()

    # Runs when the start button is pressed
    def start_callback(self, _t):
        self.log("Start pressed")
        # If not enabled, don't do anything
        if not self.enabled:
            return None

        # Log time and switch state if already running
        if self.started:
            self.total_duration[self.state] += self._elapsed_time()
            self.state = self._next_state()
            # Reset time zero
            self.log("Switched state")

        self.started = True
        self.last_reset_time = time.time()

        # Force a display update to get immediate state reflection
        self.update_display()

    # Stops
    def stop_callback(self, _t):
        self.log("Stop pressed")
        self.started = False

    def _elapsed_time(self):
        return time.time() - self.last_reset_time

    # Display current state and time
    def update_display(self):
        current_duration = self._elapsed_time()
        t = "%02d:%02d" % (current_duration //
                           3600, (current_duration/60) % 60)

        # Display time
        if t != self.last_displayed_text:
            self.display.show_text(t)
            self.last_displayed_text = t

        # Update icons
        if self.state != self.last_displayed_state:
            if self.last_displayed_state != None:
                self.display.hide_icon(
                    self.state_icons[self.last_displayed_state])
            self.display.show_icon(self.state_icons[self.state])
            self.last_displayed_state = self.state

        self.flash_colon()

    def flash_colon(self):
        if self.enabled and self.started:
            t = time.time()
            if t % 2 == 0:
                self.display.show_char(":", pos=10)
            else:
                self.display.show_char(" :", pos=10)

    def _next_state(self):
        if self.state == BabyState.awake:
            return BabyState.asleep
        return BabyState.awake
