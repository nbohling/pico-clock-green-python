import time
from scheduler import Scheduler
from clock import Clock
from apps import Apps
# from pomodoro import Pomodoro
from time_set import TimeSet
from baby_timer import BabyTimer

APP_CLASSES = [
    Clock,
    BabyTimer,
    TimeSet,
]

scheduler = Scheduler()
apps = Apps(scheduler)
for App in APP_CLASSES:
    apps.add(App(scheduler))

print("STARTING...")
scheduler.start()

while True:
    time.sleep(1)
    print(".", end="")
