import time
import os
import threading
import pygame

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def custom_clock(alarm_time):
    try: #Permet de gérer les erreurs sans couper le programme.
        user_input = input("Enter the time as HH:MM:SS : ")
        hours, minutes, seconds = map(int, user_input.split(':')) #map est une fonction qui permet d'appliquer une fonction à chaque élément d'une liste ou un tuple.
        if not (0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60):
            print("Invalid time. Please enter the time as HH:MM:SS.")
            return
    except ValueError: #Intercepte l'erreur spécifique "ValueError" retenu par try et exécute le code ci-dessous.
        print("Invalid format. Please enter the time as HH:MM:SS.")
        return
    display_time = (hours, minutes, seconds) #Transformer l'heure en tuple

    def get_current_time(): #La fonction a accès à display_time plus facilement en la mettant à l'intérieur de custom_clock. Cette fonction évite d'utiliser global.
        return display_time

    while True: #Boucle à l'intérieur de la fonction pour qu'elle soit autonome.
        clear_screen()
        print(f"{display_time[0]:02}:{display_time[1]:02}:{display_time[2]:02}") #Formatage pour que le temps se print avec toujours 2 chiffres.
        if alarm_time and display_time == alarm_time:
            threading.Thread(target=alarm_duration, args=(5, get_current_time)).start() #Thread permet de faire fonctionner plusieurs scripts en parallèle.
            alarm_time = None
        time.sleep(1)
        display_time = increment_time(display_time)

def increment_time(time_tuple):
    h, m, s = time_tuple #Décomposition du tuple.
    s += 1
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        h += 1
    if h == 24:
        h = 0
    return (h, m, s) #Retour du nouveau tuple.

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

def alarm_duration(duration, get_current_time):
    start_time = time.time()
    threading.Thread(target=play_alarm_sound, args=(duration,)).start()
    while time.time() - start_time < duration:
        clear_screen()
        display_time = get_current_time()  #Récupère l'heure actuelle via la fonction callback pour ne pas qu'elle freeze.
        print(f"{display_time[0]:02}:{display_time[1]:02}:{display_time[2]:02}")
        print("\n⏰ ALARM! It's time! ⏰")
        time.sleep(1)

def play_alarm_sound(duration):
    alarm_sound = "C:/Users/marga/Projets LaPlateforme/Python/Projets/Horloge/Clairon.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(alarm_sound)
    pygame.mixer.music.play(-1) #Rejoué automatiquement (pour les sonneries courtes)
    start_time = time.time()
    while time.time() - start_time < duration:
        time.sleep(0.1)  #Petite pause pour éviter une boucle excessive (pour les sonneries courtes)
    pygame.mixer.music.stop()

while True: #Boucle pour le choix.
    try:
        user_choice = input("Do you want to use the real time (1) or a custom one (2)? Choose 1 or 2: ")
        if not 1 <= int(user_choice) <= 2:
            print("Type only 1 or 2 without spaces.")
            continue
    except ValueError:
        print("Type only 1 or 2 without spaces.")
        continue
    alarm_time = None #Alarme set to None pour éviter des bugs au préalable.
    set_alarm_choice = input("Do you want to set an alarm? (yes or no): ").strip().lower() #Strip et Lower permettent de ne pas avoir de vérifications supplémentaire si jamais l'utilisateur rentre une majuscule ou un espace.
    if set_alarm_choice == "yes":
        alarm_time = set_alarm()

    if user_choice == "1":
        def get_real_time():
            t = time.localtime()
            return (t.tm_hour, t.tm_min, t.tm_sec) #Return d'un tuple 
        while True:
            clear_screen()
            display_time = get_real_time()
            print(f"{display_time[0]:02}:{display_time[1]:02}:{display_time[2]:02}")
            if alarm_time and display_time == alarm_time:
                threading.Thread(target=alarm_duration, args=(10, get_real_time)).start()
                alarm_time = None #Retire l'alarme pour ne pas qu'elle resonne.
            now = time.time()
            sleep_time = 1 - (now % 1)  #Pour éviter que lors de l'actualisation cela saute une seconde car time.sleep(1) ne fait pas exactement parfaitement 1 seconde.
            time.sleep(sleep_time)
    elif user_choice == "2":
        custom_clock(alarm_time)
