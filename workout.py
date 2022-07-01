#!/usr/bin/env python
import sys
import time
import threading
from pygame import mixer
import pyttsx3

# spotify api


def explain():
    print("HIIT training (High intensity interval training), is a condensed form of workout\n")
    print("It is recommended to do it 2-3 times a week\n")
    print("According to google it will burn more calories then cardio\n")
    print("Follow along with the timer and the music\n")


exercise_list = []
cooldown_list = []
stretch_list = []

filename1 = "music/hyp.mp3"
filename2 = "music/relax.mp3"
filename3 = "music/relax.mp3"

workout1 = "workouts/workout.txt"
workout2 = "workouts/stretch.txt"
workout3 = "workouts/cooldown.txt"

query1 = ""
query2 = ""

signal1 = ["p1", "s1", "q1"]
signal2 = ["p2", "s2", "q2"]

music_count = 0
pos1 = 0
pos2 = 0


def fetch_workout():
    global exercise_list, stretch_list, cooldown_list
    exercises = open(workout1, "r")
    for exercise in exercises:
        exercise.strip()
        exercise_list.append(exercise)

    stretches = open(workout2, "r")
    for stretch in stretches:
        stretch.strip()
        stretch_list.append(stretch)

    cooldownies = open(workout3, "r")
    for cooldown in cooldownies:
        cooldown.strip()
        cooldown_list.append(cooldown)


def start_time(t, action):
    global query1, query2, signal1, signal2
    if action == "rest":
        print("REST")
        query1 = "p1"
        time.sleep(1)
        query2 = "s2"
    else:
        query2 = "p2"
        time.sleep(1)
        query1 = "s1"
    while t:
        timer = '{:02d}'.format(t)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    if action == "rest":
        query2 = "p2"
    else:
        query1 = "p1"


def extra(username, act, engine):
    line = ""
    action_list = []
    if act == "cooldown":
        line = f"Let us relax {username}"
        action_list = cooldown_list
    else:
        line = f"Let us loosen up {username}"
        action_list = stretch_list
    engine.say(line)
    engine.runAndWait()
    # Starting the mixer

    # Loading the song
    mixer.music.load(filename3)

    # Setting the volume
    mixer.music.set_volume(0.7)

    # Start playing the song
    mixer.music.play(-1)

    for action in action_list:
        print(f"Current exercise: {action}")
        t = 60
        while t:
            timer = '{:02d}'.format(t)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
    print("Complete\n")
    mixer.music.stop()


def video(source, signals, section):
    global query1, query2, music_count, pos1, pos2
    # mixer.music.load(source)
    # mixer.music.set_volume(0.7)
    # mixer.music.play(-1)
    # infinite loop
    while True:
        if query1 == signals[0] and section == 1:

            # Pausing the music
            # mixer.music.pause()
            pos1 = mixer.music.get_pos()
            mixer.music.stop()
            query1 = "l1"

        elif query2 == signals[0] and section == 2:

            # Pausing the music
            mixer.music.pause()
            pos2 = mixer.music.get_pos()
            mixer.music.stop()
            query2 = "l2"

        elif query1 == signals[1] and section == 1:
            # Resuming the music
            # Loading the song
            mixer.music.load(source)
            mixer.music.set_volume(0.7)
            #
            # # Start playing the song
            mixer.music.play(-1, pos1)
            # mixer.music.unpause()
            query1 = "l1"
        elif query2 == signals[1] and section == 2:

            # Resuming the music
            # Loading the song
            mixer.music.load(source)
            #
            # # Setting the volume
            mixer.music.set_volume(0.7)
            # # Start playing the song
            mixer.music.play(-1, pos2)
            # mixer.music.unpause()
            query2 = "l2"
        elif query1 == signals[2] or query2 == signals[2]:

            # Stop the mixer
            mixer.music.stop()
            break


def workout(username, engine):
    global query1, query2, signal1, signal2
    # set intervals
    stretch_val = input("Would you like to stretch first?(y/n)")
    # stretch
    if stretch_val == "y":
        extra(username, "stretch", engine)
    engine.say(f"Let us begin. Good luck!")
    engine.runAndWait()
    # workout
    workout_time = int(input("Enter a workout time: "))
    rest_time = int(input("Enter a rest time: "))

    w1 = threading.Thread(target=video, args=(filename1, signal1, 1))
    w1.start()

    w2 = threading.Thread(target=video, args=(filename2, signal2, 2))
    w2.start()

    for exercise in exercise_list:
        print(f"Current exercise: {exercise}")
        start_time(workout_time, "workout")
        print("Complete\n")
        start_time(rest_time, "rest")
        print("Complete\n")
    print("Complete\n")

    # cooldown.mp3 / guided meditation
    engine.say(f"You did great {username}. Good Job!")
    engine.runAndWait()
    cool = input("Would you like to do a cooldown?(y/n)")
    if cool == "y":
        extra(username, "cooldown", engine)
    engine.say(f"Great workout {username}. Let us make today a great day")
    engine.runAndWait()
    query1 = "q1"
    query2 = "q2"
    mixer.quit()
    sys.exit()


if __name__ == "__main__":
    mixer.init()
    explain()
    username = input("What's your name? ")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # change to 0 for male voice. I like this one more (turn to 7 on macs)
    #engine.setProperty('voice', voices[1].id)
    engine.setProperty('voice', voices[7].id)

    engine.say(f"Hello {username} lets have a great workout")
    engine.runAndWait()
    fetch_workout()
    workout(username, engine)
    engine.stop()
