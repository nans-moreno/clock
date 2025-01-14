import time
import os
import threading
import pygame

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def choose_display_mode():
    mode_choice = input("Do you want to display the time in 12-hour mode (12) or 24-hour mode (24)? (12/24): ").strip()
    if mode_choice == '12':
        return 12
    elif mode_choice == '24':
        return 24
    else:
        print("Invalid display mode. Defaulting to 24-hour mode.")
        return 24

def format_time(hours, minutes, seconds, display_mode):
    if display_mode == 12:
        period = "AM" if hours < 12 else "PM"
        hours = hours % 12 #Division that takes the rest for a good conversion (ex : 22h = 22 % 12 = 10)
        if hours == 0:
            hours = 12
        return f"{hours:02}:{minutes:02}:{seconds:02} {period}"
    else:
        return f"{hours:02}:{minutes:02}:{seconds:02}"

def custom_clock(alarm_time, display_mode):
    try: # Allows to handle errors without stopping the program.
        user_input = input("Enter the time as HH:MM:SS : ")
        hours, minutes, seconds = map(int, user_input.split(':')) # map applies a function to each element of a list or tuple.
        if not (0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60):
            print("Invalid time. Please enter the time as HH:MM:SS.")
            return
    except ValueError: # Catches the specific "ValueError" retained by try and executes the code below.
        print("Invalid format. Please enter the time as HH:MM:SS.")
        return
    display_time = (hours, minutes, seconds) # Converts the time into a tuple

    def get_current_time(): # The function has easier access to display_time by placing it inside custom_clock.
        return display_time
    while True: # Loop inside the function to make it autonomous.
        clear_screen()
        print(format_time(display_time[0], display_time[1], display_time[2], display_mode)) # Format the time according to the chosen display mode.
        if alarm_time and display_time == alarm_time:
            threading.Thread(target=alarm_duration, args=(7, get_current_time, display_mode)).start() # Thread allows multiple scripts to run in parallel.
            alarm_time = None # Removes the alarm to prevent it from ringing again.
        time.sleep(1)
        display_time = increment_time(display_time)

def increment_time(time_tuple):
    h, m, s = time_tuple # Decomposition of the tuple.
    s += 1
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        h += 1
    if h == 24:
        h = 0
    return (h, m, s) # Returns the new tuple.

def set_alarm():
    try:
        alarm_input = input("Set the alarm time as HH:MM:SS : ")
        alarm_hours, alarm_minutes, alarm_seconds = map(int, alarm_input.split(':'))
        if not (0 <= alarm_hours < 24 and 0 <= alarm_minutes < 60 and 0 <= alarm_seconds < 60):
            print("Invalid alarm time. Please enter a valid time as HH:MM:SS.")
            return None 
        return (alarm_hours, alarm_minutes, alarm_seconds)
    except ValueError:
        print("Invalid format. Please enter the alarm time as HH:MM:SS.")
        return None

def alarm_duration(duration, get_current_time, display_mode):
    start_time = time.time()
    threading.Thread(target=play_alarm_sound, args=(duration,)).start()
    while time.time() - start_time < duration:
        clear_screen()
        display_time = get_current_time()  # Retrieves the current time via the callback function to prevent it from freezing.
        print(format_time(display_time[0], display_time[1], display_time[2], display_mode))
        print("\n\u23F0 ALARM! It's time! \u23F0")
        time.sleep(1)

def play_alarm_sound(duration):
    alarm_sound = "C:/Users/marga/Projets LaPlateforme/Python/Projets/Horloge/Clairon.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(alarm_sound)
    pygame.mixer.music.play(-1) # Automatically replay (for short ringtones)
    start_time = time.time()
    while time.time() - start_time < duration:
        time.sleep(0.1)  # Small pause to avoid excessive looping (for short ringtones)
    pygame.mixer.music.stop()

while True: # Loop for choice.
    try:
        user_choice = input("Do you want to use the real time (1) or a custom one (2)? Choose 1 or 2: ")
        if not 1 <= int(user_choice) <= 2:
            print("Type only 1 or 2 without spaces.")
            continue
    except ValueError:
        print("Type only 1 or 2 without spaces.")
        continue

    display_mode = choose_display_mode() # Ask the user for their preferred display mode (12 or 24).

    alarm_time = None # Alarm set to None to avoid bugs beforehand.
    set_alarm_choice = input("Do you want to set an alarm? (yes or no): ").strip().lower() # Strip and Lower prevent extra checks in case the user enters uppercase or spaces.
    if set_alarm_choice == "yes":
        alarm_time = set_alarm()
    else:
        print("Please enter 'yes' or 'no' only.")
        break

    if user_choice == "1":
        def get_real_time():
            t = time.localtime()
            return (t.tm_hour, t.tm_min, t.tm_sec) # Returns a tuple
        while True:
            clear_screen()
            display_time = get_real_time()
            print(format_time(display_time[0], display_time[1], display_time[2], display_mode))
            if alarm_time and display_time == alarm_time:
                threading.Thread(target=alarm_duration, args=(7, get_real_time, display_mode)).start()
                alarm_time = None # Removes the alarm to prevent it from ringing again.
            now = time.time()
            sleep_time = 1 - (now % 1)  # To avoid skipping a second during refresh as time.sleep(1) isn't exactly calculating 1 second.
            time.sleep(sleep_time)
    elif user_choice == "2":
        custom_clock(alarm_time, display_mode)
