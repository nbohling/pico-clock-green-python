import time
from scheduler import Scheduler
from clock import Clock
from apps import Apps
# from pomodoro import Pomodoro
from time_set import TimeSet
from baby_timer import BabyTimer
from logger import Logger

APP_CLASSES = [
    # Clock,
    BabyTimer,
    # TimeSet,
]

logger = Logger()
scheduler = Scheduler()
apps = Apps(scheduler, logger)
for App in APP_CLASSES:
    apps.add(App(scheduler, logger))

logger.print("STARTING...")
try:
    scheduler.start()
except Exception as e:
    logger.print("Error!")
    logger.print(e)

spinner = {
    0: "/",
    1: "-",
    2: "\\",
    3: "|"
}

spinner_ix = 0
while True:
    time.sleep(1)
    print("\b" + spinner[spinner_ix], end="")
    spinner_ix += 1
    if spinner_ix >= len(spinner):
        spinner_ix = 0
