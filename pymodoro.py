import os
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

SECONDS_IN_A_MINUTE = 60
MAIN_TIME_FRACTION = 0.8
REMAINING_TIME_FRACTION = 0.2


def install_focus_mode():
    print("Installing macos-focus-mode...")
    if os.system("npm i -g macos-focus-mode") != 0:
        print("Something went wrong. Aborting")
        exit(1)
    if os.system("macos-focus-mode install") != 0:
        print("Something went wrong. Aborting")
        exit(1)
    print("Once you've finished adding the MacOS shortcut, please launch Pymodoro again :)")
    exit(0)


res = os.system("macos-focus-mode --help")
if res != 0:
    should_install_focus_mode = input("macos-focus-mode missing, do you want to install it now? (y/n): ")
    if should_install_focus_mode == "y":
        is_npm_installed = os.system("npm -v")
        if is_npm_installed != 0:
            print("Please install nodejs and npm, e.g. using Brew: https://formulae.brew.sh/formula/node")
        else:
            print("Node and npm detected")
            install_focus_mode()
    else:
        print("Please install macos-focus-mode manually before retrying: https://github.com/arodik/macos-focus-mode")
        exit(res)


def dnd_on():
    print("DND on")
    # time.sleep(5)  # Delaying so that our notification about DND ON started appears on screen ;)
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

    root.attributes('-topmost', True)  # Make the window jump in front of other apps
    tk.mainloop()


def speak(msg):
    os.system(msg)


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


pomodoro_duration_minutes = int(sys.argv[1])
pomodoro_duration_seconds = pomodoro_duration_minutes * 60
options = sys.argv[2:]

sound_on = "--no-sound" not in options
popup_on = "--no-popup" not in options
progressbar_on = "--no-progress" not in options


if progressbar_on:
    root = tk.Tk()
    root.attributes('-topmost', True)
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Solution for the icon: https://stackoverflow.com/a/52930845/1972469
    img = tk.Image("photo", file="pymodoro.png")
    root.iconphoto(True, img)

    progress = tk.DoubleVar()
    style = ttk.Style(root)
    style.theme_use('classic')
    root.title("Pymodoro session")
    root.geometry('400x60')
    pb = ttk.Progressbar(root, orient='horizontal', mode='determinate',
                         length=380,
                         maximum=pomodoro_duration_seconds,
                         variable=progress)
    pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
    one_minute_in_millis = 1000*60
    one_second_in_millis = 1000
    minutes_in_millis = pomodoro_duration_minutes * one_minute_in_millis


    def end_pomodoro():
        root.destroy()
        if sound_on:
            x = threading.Thread(target=speak,
                                 args=("say pomodoro finished - take a break",))
            x.start()
        dnd_off()
        show_end()


    def second_elapsed(first_run: bool):
        if not first_run:
            progress.set(progress.get() + 1)  # second
            if progress.get() >= pomodoro_duration_seconds:
                end_pomodoro()
        root.after(one_second_in_millis, second_elapsed, False)


    dnd_on_thrd = threading.Thread(target=dnd_on)
    dnd_on_thrd.start()


    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to stop the Pomodoro?"):
            dnd_off()
            root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_closing)
    second_elapsed(True)
    root.mainloop()

else:
    try:
        notify_thrd = threading.Thread(target=notify,
                                       args=("Pymodoro", f"{pomodoro_duration_minutes} minutes, go go go!"))
        notify_thrd.start()

        # if sound_on:
        #     x = threading.Thread(target=speak,
        #                          args=(f"say {minutes} minutes, focus time!",))
        #     x.start()

        print(f"Pomodoro started, you have {pomodoro_duration_minutes} minutes")
        dnd_on_thrd = threading.Thread(target=dnd_on)
        dnd_on_thrd.start()

        main_minutes = round(MAIN_TIME_FRACTION * pomodoro_duration_minutes)
        remaining_minutes = round(REMAINING_TIME_FRACTION * pomodoro_duration_minutes)

        for minute in range(main_minutes):
            print(f"{pomodoro_duration_minutes - minute} minutes left")
            time.sleep(SECONDS_IN_A_MINUTE)

        # System notification
        # FIXME Experimenting
        if remaining_minutes != 0:
            if sound_on:
                x = threading.Thread(target=speak,
                                     args=(f"say {remaining_minutes} minutes left",))
                x.start()
            # os.system("macos-focus-mode disable")
            # notify("Pymodoro", f"Pomodoro: {remaining_minutes} minutes left.")
            for minute in range(remaining_minutes):
                print(f"{remaining_minutes - minute} minutes left")
                time.sleep(SECONDS_IN_A_MINUTE)
            time.sleep(5)
            # os.system("macos-focus-mode enable --silent")

        print("Pomodoro finished")
        dnd_off()
        notify("Pymodoro", f"Pomodoro finished. Take a break!")
        if sound_on:
            x = threading.Thread(target=speak,
                                 args=("say pomodoro finished - take a break",))
            x.start()
        if popup_on:
            show_end()
    except (KeyboardInterrupt, SystemExit):
        print("\n")
        dnd_off()
        print("You've successfully interrupted a pomodoro. Goodbye!")
