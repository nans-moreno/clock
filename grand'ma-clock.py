import time
import os
import threading
import keyboard
import pygame  

# Default settings
custom_time = None
alarm_time = None
display_mode = 24 
paused = False  
alarm_triggered = False  
pause_lock = threading.Lock() 

commands = """
List of commands:
- 'p' to pause
- 'r' to restart
- 'a' to cancel
- 'q' to stop
"""

def clear_screen(): 
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux/Mac
        os.system('clear')

def play_alarm_sound():
    # Run pygame
    pygame.mixer.init()
    pygame.mixer.music.load('alarm.mp3') 
    pygame.mixer.music.play()

def display_realtime():
    global custom_time, alarm_time, display_mode, paused, alarm_triggered
    try:
        while True:
            with pause_lock:
                if not paused:
                    # Check if custom time is set
                    if custom_time:
                        hours, minutes, seconds = custom_time
                    else:
                        # Get real time
                        current_time = time.localtime()
                        hours = current_time.tm_hour
                        minutes = current_time.tm_min
                        seconds = current_time.tm_sec

                    # Change time format
                    if display_mode == 12:
                        period = "AM" if hours < 12 else "PM"
                        display_hours = hours % 12
                        if display_hours == 0:
                            display_hours = 12
                        formatted_time = f"{display_hours:02}:{minutes:02}:{seconds:02} {period}"
                    else:
                        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"

                    # Clear the screen
                    clear_screen()

                    # Print the time
                    print(formatted_time)

                    # Check if current time matches alarm time
                    if alarm_time and (hours, minutes, seconds) == alarm_time:
                        alarm_triggered = True
                        play_alarm_sound()  # Play alarm sound

                    if alarm_triggered:
                        print("\nALARM!!! It's time to wake up!")

                    # Update seconds for custom time
                    if custom_time:
                        seconds += 1
                        if seconds >= 60:
                            seconds = 0
                            minutes += 1
                        if minutes >= 60:
                            minutes = 0
                            hours += 1
                        if hours >= 24:
                            hours = 0
                        custom_time = (hours, minutes, seconds)

            # Print the list of commands
            print(commands)

            # Wait one second
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop with Ctrl+C
        print("\nProgram stopped by the user.")

def set_custom_time(hours, minutes, seconds):
    global custom_time
    # Set custom time
    custom_time = (hours, minutes, seconds)

def set_alarm(hours, minutes, seconds):
    global alarm_time
    # Set alarm time
    alarm_time = (hours, minutes, seconds)

def choose_display_mode():
    global display_mode
    # Ask the user to choose time format
    mode = input("Do you want to display the time in 12-hour (12) or 24-hour (24) format? (12/24): ").strip()
    if mode == '12':
        display_mode = 12
    elif mode == '24':
        display_mode = 24
    else:
        print("Invalid display mode. Defaulting to 24-hour mode.")
        display_mode = 24

def pause_clock():
    global paused
    with pause_lock:
        # Pause the clock
        paused = True
        print("Clock paused.")

def restart_clock():
    global paused
    with pause_lock:
        # Restart the clock
        paused = False
        print("Clock resumed.")

def cancel_alarm():
    global alarm_triggered
    # Cancel the alarm
    alarm_triggered = False
    pygame.mixer.music.stop()  # Stop the alarm sound
    print("Alarm canceled.")

def main():
    # Ask the user whether to use current time or set custom time
    choice = input("Do you want to use the current time (c) or set a custom time (s)? (c/s): ").strip().lower()

    if choice == 's':
        # Ask the user to set custom time
        try:
            hours = int(input("Enter hours (0-23): "))
            minutes = int(input("Enter minutes (0-59): "))
            seconds = int(input("Enter seconds (0-59): "))
            set_custom_time(hours, minutes, seconds)
        except ValueError:
            print("Please enter valid numeric values.")
            return

    # Ask the user if they want to set an alarm
    set_alarm_choice = input("Do you want to set an alarm? (y/n): ").strip().lower()
    if set_alarm_choice == 'y':
        try:
            alarm_hours = int(input("Enter alarm hours (0-23): "))
            alarm_minutes = int(input("Enter alarm minutes (0-59): "))
            alarm_seconds = int(input("Enter alarm seconds (0-59): "))
            set_alarm(alarm_hours, alarm_minutes, alarm_seconds)
        except ValueError:
            print("Please enter valid numeric values.")
            return

    # Ask the user to choose display mode
    choose_display_mode()

    # Start the real-time clock
    display_thread = threading.Thread(target=display_realtime)
    display_thread.start()

    # Command loop
    while True:
        if keyboard.is_pressed('p'):
            pause_clock()
        elif keyboard.is_pressed('r'):
            restart_clock()
        elif keyboard.is_pressed('a'):
            cancel_alarm()
        elif keyboard.is_pressed('q'):
            break
        time.sleep(0.1)  

    display_thread.join()

if __name__ == "__main__":
    main()
