import os
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk

SECONDS_IN_A_MINUTE = 60
MAIN_TIME_FRACTION = 0.8
REMAINING_TIME_FRACTION = 0.2


def dnd_on():
    print("DND on")
    time.sleep(5)  # Delaying so that our notification about DND ON started appears on screen ;)
    os.system("macos-focus-mode enable --silent")


def dnd_off():
    print("DND off")
    os.system("macos-focus-mode disable")


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


def speak(msg):
    os.system(msg)


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


minutes = int(sys.argv[1])
options = sys.argv[2:]

sound_on = "--no-sound" not in options
popup_on = "--no-popup" not in options

root = tk.Tk()
style = ttk.Style(root)
print(style.theme_names())
style.theme_use('classic')
root.title("Pymodoro session")
root.geometry('400x60')
pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=380, maximum=minutes)
pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
# pb.pack()
# pb.after(1000, lambda: _ )
# for minute in range(minutes):
#     time.sleep(SECONDS_IN_A_MINUTE)
#     pb['value'] += 10
# tk.mainloop()
# TODO: use this: https://stackoverflow.com/a/36520333/1972469
one_minute_in_millis = 500
minutes_in_millis = minutes * one_minute_in_millis


def end_pomodoro():
    root.destroy()
    show_end()


def minute_elapsed(first_run: bool):
    if not first_run:
        if pb['value'] >= minutes:
            end_pomodoro()
        pb['value'] += 1
        root.update_idletasks()
    root.after(one_minute_in_millis, minute_elapsed, False)


minute_elapsed(True)
root.mainloop()



# try:
#     # progress_thrd = threading.Thread(target=show_progress)
#     # progress_thrd.start()
#     # show_progress()
#
#     notify_thrd = threading.Thread(target=notify, args=("Pymodoro", f"{minutes} minutes, go go go!"))
#     notify_thrd.start()
#
#     # if sound_on:
#     #     x = threading.Thread(target=speak,
#     #                          args=(f"say {minutes} minutes, focus time!",))
#     #     x.start()
#
#     print(f"Pomodoro started, you have {minutes} minutes")
#     dnd_on_thrd = threading.Thread(target=dnd_on)
#     dnd_on_thrd.start()
#
#     main_minutes = round(MAIN_TIME_FRACTION * minutes)
#     remaining_minutes = round(REMAINING_TIME_FRACTION * minutes)
#
#     for minute in range(main_minutes):
#         print(f"{minutes - minute} minutes left")
#         time.sleep(SECONDS_IN_A_MINUTE)
#
#     # System notification
#     # FIXME Experimenting
#     if remaining_minutes != 0:
#         if sound_on:
#             x = threading.Thread(target=speak,
#                                  args=(f"say {remaining_minutes} minutes left",))
#             x.start()
#         # os.system("macos-focus-mode disable")
#         # notify("Pymodoro", f"Pomodoro: {remaining_minutes} minutes left.")
#         for minute in range(remaining_minutes):
#             print(f"{remaining_minutes - minute} minutes left")
#             time.sleep(SECONDS_IN_A_MINUTE)
#         time.sleep(5)
#         # os.system("macos-focus-mode enable --silent")
#
#     print("Pomodoro finished")
#     dnd_off()
#     notify("Pymodoro", f"Pomodoro finished. Take a break!")
#     if sound_on:
#         x = threading.Thread(target=speak,
#                              args=("say pomodoro finished - take a break",))
#         x.start()
#     if popup_on:
#         show_end()
# except (KeyboardInterrupt, SystemExit):
#     print("\n")
#     dnd_off()
#     print("You've successfully interrupted a pomodoro. Goodbye!")
