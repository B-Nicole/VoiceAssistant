import speech_recognition as sr # for voice commands
import pyttsx3 # for voice interaction
import wikipedia # for wikipedia search
import pyjokes 
import requests
import pyaudio
import subprocess #used for terminaing applications

import samsung_control

import time
import os 
import webbrowser
from random import choice 
from datetime import datetime
from decouple import config


#IMPORTANT:
USERNAME = os.environ.get('USER')
ASSISTANT_NAME = os.environ.get('ASSISTANTNAME')
 
i = 0
choice_confifrmation = [
    "I'm on it.",
    "Okay, I'm working on it.",
    "Just a second.",
    "Just a moment please.",
    "Yes"
]

'''
This function sets up the bots ability to speak and take in commands
We are using Microsoft Speech API to do this 
'''
def speak(text):
    # This function is for speaking text.
    engine = pyttsx3.init('sapi5') # Microsoft Speech API
    engine.setProperty('volume', 1.0) # set volume
    engine.setProperty('rate', 150) # set speech rate


    # Set the voice to use for speaking
    # [0] = male voice / [1] = female voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    engine.say(text)

    # processing all of the commands that are queued 
    engine.runAndWait() 

'''
    This fuction set up a basic greeting and then waits for the user to enter a command
'''
def Greeting():
    # This function will greet the user by name and depending on the time of day
    hour = datetime.now().hour
    if hour >= 0 and hour < 12: 
        speak(f"Good Morning {USERNAME}")
    elif hour >= 12 and hour < 18:
        speak(f"Good Afternoon {USERNAME}")
    else:
        speak(f"Good Evening {USERNAME}") 
    speak("I am " + ASSISTANT_NAME)

def takeCommand(): 
    global i 
    # this function takes in user input and converts it to text
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        i = 0
        return query
    
    except Exception: 
        i = i + 1
        if i < 3:
            speak("again please...")
            takeCommand()   
        else:
            speak("I'm sorry, I could not understand. Goodbye")
        return "None"


def executeCommand():
    speak("What can I do for you?")
    query = takeCommand().lower()

    print(query)
    if  any(x in query for x in ['bye', 'quit', 'exit']):
        speak("Goodbye")
        exit()

    if any(x in query for x in ['time', 'whats the current time', 'what time is it']):
        speak(choice(choice_confifrmation))
        tellTime()
    elif any(x in query for x in ['day', 'whats the current day', 'what day is it', 'what day is it today', 'what day of the week is it']):
        speak(choice(choice_confifrmation))
        tellDay()
    elif any(x in query for x in ['joke','tell me a joke', 'got a joke', 'tell me something funny']):
        speak(choice(choice_confifrmation))
        tellJoke()
    elif any(x in query for x in ['open', 'launch', 'start', 'open up', 'search', 'google']):
        open_application(query)
    else:
        speak("I'm sorry, I could not understand. Goodbye")
        exit()
    return

  
''' _________________ BELOW ARE FUNCTION OF THE ASSISTANT _________________ '''


def open_application(input):
  
    if "firefox" in input or "mozilla" in input:
        try:
            speak("Opening Firefox")
            os.startfile('C:\Program Files (x86)\Mozilla Firefox\\firefox.exe')
            executeCommand()
        except Exception: 
            speak("Sorry, I can not open that application at this time")
            exit()
  
    elif "clip studio" in input or "studio" in input:
        try:
            speak("Opening Clip Studio")
            os.startfile('C:\Program Files\CELSYS\CLIP STUDIO 1.5\CLIP STUDIO PAINT\CLIPStudioPaint.exe')
            executeCommand()
            
        except Exception: 
            speak("Sorry, I can not open that application at this time")
            exit()

    elif "pictures" in input:
        try:
            speak("Opening Pictures")
            os.system("Pictures")
            executeCommand()

        except Exception: 
            speak("Sorry, I can not open that application at this time")
            exit()

    elif "search youtube" in input:
        try:
            search_term = input.split("for")[-1]  
            url = f"https://www.youtube.com/results?search_query={search_term}"  
            webbrowser.open_new_tab(url) 
            speak(f'Here is what I found for {search_term} on youtube')
            executeCommand()

        except Exception: 
            speak("Sorry, I can not open that application at this time")
            exit()

    elif "google" in input or 'search' in input:
        try:
            search_term = input.split("for")[-1]  
            url = f"https://google.com/search?q={search_term}"  
            webbrowser.open_new_tab(url)    
            speak(f'Here is what I found for {search_term} on google')
            executeCommand() 

        except Exception:
            speak("Sorry, I can not open that application at this time")
            exit()

    elif "reddit" in input:
        try:
            speak("Opening Reddit") 
            url ="https://www.reddit.com/"  
            webbrowser.open_new_tab(url)    
            executeCommand()

        except Exception:
            speak("Sorry, I can not open that application at this time")
            exit()
    else:
        speak("I'm sorry, I could not understand. Goodbye")
        exit()



def tellTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak(f"The time is {current_time}")
    executeCommand()

def tellDay():
    day = datetime.today().weekday() + 1
      
    #this line tells us about the number 
    # that will help us in telling the day
    Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday',7: 'Sunday'}
      
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        speak("Today is " + day_of_the_week)

    executeCommand()


def tellJoke():
    speak(pyjokes.get_joke())
    executeCommand()
    return

 

if __name__ == "__main__":
    Greeting()
    executeCommand()
    # This is the main function that will run the program
    # We will be using the microphone to take in the commands