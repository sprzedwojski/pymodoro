import os
import sys
import time
import tkinter as tk

SECONDS_IN_A_MINUTE = 60
MAIN_TIME_FRACTION = 0.8
REMAINING_TIME_FRACTION = 0.2


def dnd_on():
    print("DND on")
    os.system("do-not-disturb on")


def dnd_off():
    print("DND off")
    os.system("do-not-disturb off")


def show_end():
    root = tk.Tk()
    root.title("Pymodoro")
    window_width = 800
    window_height = 500
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
    # Positions the window in the center of the page.
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, position_right, position_down))
    label = tk.Label(root, text="Pomodoro finished.\nTake a break!")
    label.place(x=window_width/2, y=window_height/2, anchor="center")
    label.config(font=("Courier", 60))
    tk.mainloop()


minutes = int(sys.argv[1])
options = sys.argv[2:]

sound_on = "--no-sound" not in options
popup_on = "--no-popup" not in options

try:
    print(f"Pomodoro started, you have {minutes} minutes")
    dnd_on()
    if sound_on:
        os.system(f"say pomodoro started, you have {minutes} minutes, DND on")

    main_minutes = round(MAIN_TIME_FRACTION * minutes)
    remaining_minutes = round(REMAINING_TIME_FRACTION * minutes)

    for minute in range(main_minutes):
        print(f"{minutes - minute} minutes left")
        time.sleep(SECONDS_IN_A_MINUTE)

    if sound_on:
        os.system(f"say {remaining_minutes} minutes left in the pomodoro")

    for minute in range(remaining_minutes):
        print(f"{remaining_minutes - minute} minutes left")
        time.sleep(SECONDS_IN_A_MINUTE)

    print("Pomodoro finished")
    dnd_off()
    if sound_on:
        os.system("say DING DING DING, pomodoro finished, DND off - take a break")
    if popup_on:
        show_end()
except (KeyboardInterrupt, SystemExit):
    print("\n")
    dnd_off()
    print("You've successfully interrupted a pomodoro. Goodbye!")
