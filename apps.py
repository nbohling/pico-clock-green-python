from buttons import Buttons
from display import Display


class App:
    def __init__(self, name, label, logger):
        self.name = name
        self.label = label
        self.active = False
        self.grab_top_button = False
        self.logger = logger

    def top_button(self, t):
        self.log("top_button not implemented for " + self.name)

    def log(self, message):
        self.logger.log(message)

class Apps:
    def __init__(self, scheduler, logger):
        self.display = Display(scheduler)
        self.buttons = Buttons(scheduler)
        self.apps = []
        self.current_app = 0
        # Short press to go to the next app
        self.buttons.add_callback(1, self.next, max=500)
        # Short press to go to the previous app
        self.buttons.add_callback(1, self.previous, min=500, max=1000)
        # Long press to "exit"
        self.buttons.add_callback(1, self.exit, min=1000)
        self.logger = logger

    def add(self, app):
        if len(self.apps) == 0:
            app.enable()
        self.apps.append(app)

    def next(self, t):
        self.log("NEXT")
        if len(self.apps) == 0:
            return

        app = self.apps[self.current_app]
        if app.active:
            print ("Active!")
        if app.grab_top_button:
            print ("Grab top button")
        if app.active and app.grab_top_button:
            print("Calling top button")
            app.top_button(t)
            return

        print("Didn't call top button")
        self.apps[self.current_app].disable()
        self.buttons.clear_callbacks(2)
        self.buttons.clear_callbacks(3)
        self.display.clear()
        self.current_app = (self.current_app + 1) % len(self.apps)
        self.log("SWITCHING TO", self.apps[self.current_app].name)
        self.apps[self.current_app].enable()

    def previous(self, t):
        self.log("PREVIOUS")
        if len(self.apps) > 0:
            self.apps[self.current_app].disable()
            self.current_app = (self.current_app - 1) % len(self.apps)
            self.apps[self.current_app].enable()

    def exit(self, t):
        self.log("EXIT")
        if len(self.apps) > 0:
            self.apps[self.current_app].disable()
            self.current_app = 0
            self.apps[self.current_app].enable()

    def log(self, message):
        self.logger.log(message)
