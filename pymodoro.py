import os
import sys
import time

SECONDS_IN_A_MINUTE = 60
MAIN_TIME_FRACTION = 0.8
REMAINING_TIME_FRACTION = 0.2


def dnd_on():
    print("DND on")
    os.system("do-not-disturb on")


def dnd_off():
    print("DND off")
    os.system("do-not-disturb off")


minutes = int(sys.argv[1])

try:
    print(f"Pomodoro started, you have {minutes} minutes")
    dnd_on()
    os.system(f"say pomodoro started, you have {minutes} minutes, DND on")

    main_minutes = round(MAIN_TIME_FRACTION * minutes)
    remaining_minutes = round(REMAINING_TIME_FRACTION * minutes)

    for minute in range(main_minutes):
        print(f"{minutes - minute} minutes left")
        time.sleep(SECONDS_IN_A_MINUTE)

    os.system(f"say {remaining_minutes} minutes left in the pomodoro")

    for minute in range(remaining_minutes):
        print(f"{remaining_minutes - minute} minutes left")
        time.sleep(SECONDS_IN_A_MINUTE)

    print("Pomodoro finished")
    dnd_off()
    os.system("say DING DING DING, pomodoro finished, DND off - take a break")
except (KeyboardInterrupt, SystemExit):
    print("\n")
    dnd_off()
    print("You've successfully interrupted a pomodoro. Goodbye!")
