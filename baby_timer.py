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

        self.grab_top_button = True

        # Callback that drives update
        scheduler.schedule("time-second", 1000, self.update_display_callback)

    def enable(self):
        self.enabled = True
        self.active = True
        self.buttons.add_callback(2, self.start_callback, max=500)
        self.buttons.add_callback(3, self.remove_time, max=500)

    def disable(self):
        self.enabled = False
        self.active = False
        self.buttons.remove_callback(2, self.start_callback, max=500)
        # self.buttons.remove_callback(3, self.stop_callback, max=500)

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

        self.total_duration[self.state] += self._elapsed_time()
        self.state = self._next_state()
        # Reset time zero
        self.log("Switched state")

        self.last_reset_time = time.time()

        # Force a display update to get immediate state reflection
        self.update_display()

    def top_button(self, _t):
        self.add_time()

    def add_time(self):
        # Move the reset clock back 1 minute
        self.last_reset_time = self.last_reset_time - 60

        # Force a display update to get immediate state reflection
        self.update_display()


    def remove_time(self, _t):
        # Move the reset clock forward 1 minute
        new_reset_time = self.last_reset_time + 60
        if new_reset_time < time.time():
            self.last_reset_time = new_reset_time
            # Force a display update to get immediate state reflection
            self.update_display()

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
        if self.enabled:
            t = time.time()
            if t % 2 == 0:
                self.display.show_char(":", pos=10)
            else:
                self.display.show_char(" :", pos=10)

    def _next_state(self):
        if self.state == BabyState.awake:
            return BabyState.asleep
        return BabyState.awake
