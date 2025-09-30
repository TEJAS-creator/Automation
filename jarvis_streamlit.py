import speech_recognition as sr
import pyttsx3
import datetime
import subprocess
import webbrowser
import pyautogui
import psutil
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import requests
from bs4 import BeautifulSoup
import pygetwindow as gw
import openai
import wikipedia
import os
import pywhatkit
import time

# --------- INIT ---------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

OPENAI_API_KEY = 'Your_API_Key'
openai.api_key = OPENAI_API_KEY
NEWS_API_KEY = 'defb8ed0610f4a36ad2c189219fc2773'


# --------- HELPERS ---------
def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    try:
        print("Recognizing...")
        return recognizer.recognize_google(audio, language='en-in').lower()
    except:
        return "None"

def query_gpt3(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            max_tokens=100,
            temperature=0.5
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {e}"

def adjust_volume(change):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    new_volume = max(0.0, min(1.0, volume.GetMasterVolumeLevelScalar() + change))
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    return f"Volume set to {int(new_volume * 100)} percent"

def get_news(query=None):
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    if query:
        url += f"&q={query}"
    try:
        data = requests.get(url).json()
        return [a['title'] for a in data.get('articles', [])[:5]] or ["No news found."]
    except Exception as e:
        return [f"Error: {e}"]


# --------- MAIN BRAIN ---------
def process_command(command: str) -> str:
    command = command.lower()
    response = "I didn’t understand that."

    try:
        if "time" in command:
            response = datetime.datetime.now().strftime("The time is %I:%M %p")

        elif "date" in command:
            response = datetime.datetime.now().strftime("Today is %A, %B %d, %Y")

        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            if topic:
                response = wikipedia.summary(topic, sentences=3)
            else:
                response = "Give me a topic to search on Wikipedia."

        elif "google" in command:
            topic = command.replace("google", "").strip()
            if topic:
                headers = {"User-Agent": "Mozilla/5.0"}
                r = requests.get(f"https://www.google.com/search?q={topic}", headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                results = soup.find_all('div', class_='BNeawe')
                response = results[0].text if results else "No info found."
            else:
                response = "What do you want to search?"

        elif "news" in command:
            response = "\n".join(get_news())

        elif "youtube" in command and "play" in command:
            song = command.replace("play", "").replace("on youtube", "").strip()
            pywhatkit.playonyt(song)
            response = f"Playing {song} on YouTube."

        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com/")
            response = "Opening YouTube."

        elif "open chrome" in command:
            subprocess.Popen(["C:/Program Files/Google/Chrome/Application/chrome.exe"])
            response = "Opening Chrome."

        elif "notepad" in command:
            subprocess.Popen("notepad.exe")
            response = "Opening Notepad."

        elif "vlc" in command:
            subprocess.Popen("C:/Program Files/VideoLAN/VLC/vlc.exe")
            response = "Opening VLC Player."

        elif "shutdown" in command:
            subprocess.call(["shutdown", "/s", "/t", "0"])
            response = "Shutting down the system."

        elif "brightness up" in command:
            sbc.set_brightness("+10")
            response = "Increased brightness by 10%."

        elif "brightness down" in command:
            sbc.set_brightness("-10")
            response = "Decreased brightness by 10%."

        elif "battery" in command:
            battery = psutil.sensors_battery()
            response = f"Battery is at {battery.percent}%."

        elif "volume up" in command:
            response = adjust_volume(0.1)

        elif "volume down" in command:
            response = adjust_volume(-0.1)

        elif "gpt" in command or "artificial" in command:
            response = query_gpt3(command)

        elif command in ["exit", "quit", "bye"]:
            response = "Goodbye!"

    except Exception as e:
        response = f"Error: {str(e)}"

    # Jarvis speaks + returns text
    speak(response)
    return response


# --------- RUN (for terminal use) ---------
if __name__ == "__main__":
    speak("Jarvis initialized. Say a command.")
    while True:
        cmd = input("You: ")
        reply = process_command(cmd)
        print("Jarvis:", reply)
        if reply == "Goodbye!":
            break
