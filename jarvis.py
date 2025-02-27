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
import json
import pygetwindow as gw
import cv2  # Import OpenCV for capturing photos
import openai
import wikipedia  # Import the Wikipedia library
import os
import pywhatkit
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Check if there are enough voices
if len(voices) >= 3:
    engine.setProperty('voice', voices[0].id)  # Set the third voice
else:
    engine.setProperty('voice', voices[0].id)  # Set the default voice     1=female    0=male

# Set your OpenAI API key
OPENAI_API_KEY = 'Your_API_Key'
openai.api_key = OPENAI_API_KEY    

# Function to speak out text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech using Google Speech Recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)   # used to make jarvis respond

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please say that again.")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "None"
    return query.lower()

# Function to query GPT-3.5-turbo
def query_gpt3(query):
    try:
        print(f"Querying GPT-3.5 with: {query}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5
        )
        print(f"Response: {response}")
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}" 

# Function to handle media control
def control_media(command):
    if command == "play":
        pyautogui.press('playpause')
    elif command == "pause":
        pyautogui.press('playpause')
    elif command == "next":
        pyautogui.press('nexttrack')
    elif command == "previous":
        pyautogui.press('prevtrack')

# Function to adjust system volume
def adjust_volume(change):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, min(1.0, current_volume + change))
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    speak(f"Volume set to {int(new_volume * 100)} percent")

# Function to get information from the web
def get_web_info(query):
    try:
        response = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json")
        if response.status_code == 200:
            data = response.json()
            answer = data.get('AbstractText')
            if not answer:
                related_topics = data.get('RelatedTopics', [])
                if related_topics:
                    answer = related_topics[0].get('Text', 'No relevant information found.')
                else:
                    answer = 'No relevant information found.'
            return answer
        else:
            return "I'm sorry, I couldn't retrieve the information."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to get Wikipedia information
def get_wikipedia_info(query):
    try:
        summary = wikipedia.summary(query, sentences=50)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"There are multiple results for '{query}', please be more specific."
    except wikipedia.exceptions.PageError:
        return f"No results found for '{query}'."
    except Exception as e:
        return f"An error occurred: {e}"  

# Function to get information from Google search
def get_google_info(query):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the first snippet of text from the search results
        results = soup.find_all('div', class_='BNeawe')
        if results:
            return [result.text for result in results[:100]]  # Get top 5 snippets
        else:
            return ["No relevant information found."]
    except Exception as e:
        return [f"An error occurred: {e}"]        
        
# Function to switch to the next window
def switch_to_next_window():
    windows = gw.getAllTitles()
    current_window = gw.getActiveWindow()
    if current_window is not None:
        current_index = windows.index(current_window.title)
        next_index = (current_index + 1) % len(windows)
        gw.getWindowsWithTitle(windows[next_index])[0].activate()
        speak(f"Switched to {windows[next_index]}")
    else:
        speak("No active window found")

# Function to switch to the previous window
def switch_to_previous_window():
    windows = gw.getAllTitles()
    current_window = gw.getActiveWindow()
    if current_window is not None:
        current_index = windows.index(current_window.title)
        previous_index = (current_index - 1) % len(windows)
        gw.getWindowsWithTitle(windows[previous_index])[0].activate()
        speak(f"Switched to {windows[previous_index]}")

# Function to capture a screenshot
def capture_screenshot():
    speak("Capturing screenshot")
    screenshot = pyautogui.screenshot()
    filename = f"screenshot_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    screenshot.save(filename)
    speak(f"Screenshot saved as {filename}")

# Add your News API key here
NEWS_API_KEY = 'defb8ed0610f4a36ad2c189219fc2773'

# Function to get news
def get_news(query=None):
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
        if query:
            url += f"&q={query}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            if not articles:
                return "No news articles found."
            
            news_list = []
            for article in articles[:5]:  # Get top 5 articles
                news_list.append(article['title'])
            return news_list
        else:
            return "I'm sorry, I couldn't retrieve the news."
    except Exception as e:
        return f"An error occurred: {e}"          

# Function to handle commands based on voice input
def jarvis():
    speak("Initializing jarvis")
    #  # Password setup
    # PASSWORD = "gemini"  # Replace this with your desired password
    # speak("Please provide the password to access jarvis")
    # user_input = recognize_speech()

    # if user_input != PASSWORD:
    #     speak("Incorrect password. Access denied.")
    #     return

    while True:
        query = recognize_speech()

        if 'jarvis' in query:
            speak("Yes")
            query = recognize_speech()  # Listen for the actual command after the wake word

            if 'time' in query:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The current time is {current_time}")

            elif 'date' in query:
                current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                speak(f"Today's date is {current_date}")      

            elif 'open notepad' in query:
                speak("Opening Notepad")
                subprocess.Popen(['notepad.exe'])

            elif 'type in notepad' in query:
                speak("What should I type?")
                text_to_type = recognize_speech()
                if text_to_type != "None":
                    speak(f"Typing '{text_to_type}' in Notepad")
                    pyautogui.typewrite(text_to_type)

            elif 'close notepad' in query:
                for proc in psutil.process_iter():
                    if proc.name() == "notepad.exe":
                        proc.terminate()
                        speak("Notepad closed")        

            elif 'open calculator' in query:
                speak("Opening Calculator")
                subprocess.Popen(['calc.exe'])

            elif 'open command prompt' in query:
                speak("Opening Command Prompt")
                subprocess.Popen(['cmd.exe'])

            elif 'open chrome' in query:
                speak("Opening Chrome")
                subprocess.Popen(["C:/Program Files/Google/Chrome/Application/chrome.exe"])
    

            elif 'open youtube' in query:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com/")

            elif 'open chat' in query:
                speak("Opening ChatGPT")
                webbrowser.open("https://www.chatgpt.com/")
            
            elif 'open adobe' in query:
                speak("Opening Adobe Acrobat")
                subprocess.Popen(["C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe"])

            elif 'open music' in query:
                speak("Opening Music")
                webbrowser.open("https://wynk.in/music/my-music")

            elif 'open explorer' in query:
                speak("Opening File Explorer")
                subprocess.Popen(['explorer.exe'])

            elif 'open media player' in query:
                speak("Opening Windows Media Player Legacy")
                subprocess.Popen(["C:/Program Files/Windows Media Player/wmplaykker.exe"])

            elif 'play media player' in query:
                speak("Playing Windows Media Player Legacy")
                pyautogui.press('play')

            elif 'pause media player' in query:
                speak("Pausing Windows Media Player Legacy")
                pyautogui.press('pause')

            elif 'stop media player' in query:
                speak("Stopping Windows Media Player Legacy")
                pyautogui.press('stop')

            elif 'open word' in query:
                speak("Opening Microsoft Word")
                subprocess.Popen(["C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE"])

            elif 'open excel' in query:
                speak("Opening Microsoft Excel")
                subprocess.Popen(["C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE"])

            elif 'open powerpoint' in query:
                speak("Opening Microsoft PowerPoint")
                subprocess.Popen(["C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE"])

            elif 'open photos' in query:
                speak("Opening Photos")
                subprocess.Popen(['explorer', 'shell:PicturesLibrary'])

            elif 'open paint' in query:
                speak("Opening Paint")
                subprocess.Popen(['mspaint.exe'])

            elif 'open settings' in query:
                speak("Opening Settings")
                subprocess.Popen(['control.exe'])

            elif 'play music' in query or 'play song' in query:
                speak("Playing music")
                control_media("play")

            elif 'pause music' in query or 'pause song' in query:
                speak("Pausing music")
                control_media("pause")

            elif 'next song' in query or 'next track' in query:
                speak("Playing next song")
                control_media("next")

            elif 'previous song' in query or 'previous track' in query:
                speak("Playing previous song")
                control_media("previous")

            elif 'increase volume' in query:
                speak("Increasing volume")
                adjust_volume(0.1)

            elif 'decrease volume' in query:
                speak("Decreasing volume")
                adjust_volume(-0.1)

            elif 'internet search' in query or 'search internet' in query or 'browse' in query or 'internet' in query:
                speak("What would you like to search for?")
                search_query = recognize_speech()
                if search_query != "None":
                    speak("Searching the web...")
                    answer = get_web_info(search_query)
                    speak(answer)

            elif 'switch to next tab' in query:
                speak("Switching to the next tab")
                pyautogui.hotkey('ctrl', 'tab')

            elif 'switch to previous tab' in query:
                speak("Switching to the previous tab")
                pyautogui.hotkey('ctrl', 'shift', 'tab')

            elif 'switch to next window' in query:
                switch_to_next_window()

            elif 'switch to previous window' in query:
                switch_to_previous_window()

            elif 'take screenshot' in query:
                capture_screenshot()

            elif 'open task manager' in query:
                speak("Opening Task Manager")
                subprocess.Popen(["taskmgr"])

            elif 'open vlc' in query:
                speak("Opening VLC Media Player")
                subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe"])

            elif 'open drive' in query:
                speak("Opening Google Drive")
                webbrowser.open("https://drive.google.com/drive/u/0/my-drive")

            elif 'open amazon' in query:
                speak("Opening Amazon")
                webbrowser.open("https://www.amazon.in/")

            elif 'open calendar' in query:
                speak("Opening Google Calendar")
                webbrowser.open("https://calendar.google.com/calendar/r")

            elif 'open contacts' in query:
                speak("Opening Google Contacts")
                webbrowser.open("https://contacts.google.com/")

            elif 'open gmail' in query:
                speak("Opening Gmail")
                webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
 

            elif 'search youtube' in query:
                speak("What do you want to search for on YouTube?")
                search_query = recognize_speech()
                if search_query != "None":
                    speak(f"Searching YouTube for {search_query}")
                    webbrowser.open("https://www.youtube.com/")
                    pyautogui.sleep(8)  # Give the browser time to open YouTube
                    pyautogui.click(782, 225)  # Click on the search bar (coordinates may vary)
                    pyautogui.typewrite(search_query)
                    pyautogui.press('enter')
            
            elif 'song' in query:
                speak("Which song do you want to play?")
                search_query = recognize_speech()
                if search_query != "None":
                    speak(f"Playing song {search_query}")
                    webbrowser.open("https://www.youtube.com/")
                    pyautogui.sleep(8)  # Give the browser time to open YouTube
                    pyautogui.click(782, 225)  # Click on the search bar (coordinates may vary)
                    pyautogui.typewrite(search_query)
                    pyautogui.press('enter')
                    pyautogui.sleep(3)
                    pyautogui.click(543, 545)
                    

            elif 'search chrome' in query:
                speak("What do you want to search for on Chrome?")
                search_query = recognize_speech()
                if search_query != "None":
                    speak(f"Searching Chrome for {search_query}")
                    webbrowser.open("C:/Program Files/Google/Chrome/Application/chrome.exe")
                    pyautogui.sleep(8)  # Give the browser time to open Chrome
                    pyautogui.click(835, 95)  # Click on the search bar (coordinates may vary)
                    pyautogui.typewrite(search_query)
                    pyautogui.press('enter')
            
            elif 'search chat' in query:
                speak("What do you want to search for on ChatGPT?")
                search_query = recognize_speech()
                if search_query != "None":
                    speak(f"Searching ChatGPT for {search_query}")
                    webbrowser.open("https://chatgpt.com/")
                    pyautogui.sleep(8)  # Give the browser time to open Chrome
                    pyautogui.click(734, 994)  # Click on the search bar (coordinates may vary)
                    pyautogui.typewrite(search_query)
                    pyautogui.press('enter')
            
            elif 'search google' in query:
                speak("What do you want to search for on google?")
                search_query = recognize_speech()
                if search_query != "None":
                    speak(f"Searching google for {search_query}")
                    webbrowser.open("https://www.google.com/")
                    pyautogui.sleep(8)  # Give the browser time to open google
                    pyautogui.click(835, 95)  # Click on the search bar (coordinates may vary)
                    pyautogui.typewrite(search_query)
                    pyautogui.press('enter')

            elif 'battery' in query:
                battery = psutil.sensors_battery()
                percent = battery.percent
                speak(f"Battery is at {percent} percent")

            elif 'shutdown' in query:
                speak("Shutting down the system")
                subprocess.call(["shutdown", "/s", "/t", "0"])

            elif 'restart' in query:
                speak("Restarting the system")
                subprocess.call(["shutdown", "/r", "/t", "0"])

            elif 'sleep' in query:
                speak("Putting the system to sleep")
                subprocess.call(["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"])        

            elif 'automate' in query:             # AUTOMATION
                speak("What do you want to automate on Chrome?")
                search_query = recognize_speech()
                if search_query != "None":
                    speak(f"Automating Chrome  {search_query}")
                    webbrowser.open("C:/Program Files/Google/Chrome/Application/chrome.exe")
                    pyautogui.sleep(5)  # Give the browser time to open Chrome
                    pyautogui.click(835, 95)  # Click on the search bar (coordinates may vary)
                    pyautogui.typewrite(search_query)
                    pyautogui.press('enter')
                    pyautogui.sleep(8)  # Give the browser time to open Chrome
                    pyautogui.click(1804, 231)  # Click on the search bar (coordinates may vary)
                    pyautogui.typewrite(search_query)
                    pyautogui.press('enter')
                    pyautogui.sleep(8)  # Give the browser time to open Chrome
                    pyautogui.click(1734, 525)  # Click on the search bar (coordinates may vary)
                    pyautogui.typewrite(search_query)
                    pyautogui.press('enter')        

            elif 'open whatsapp' in query:
                    speak("Opening WhatsApp")
                    webbrowser.open("https://web.whatsapp.com/")         


# PLaying music                         
            elif 'play faded' in query:
                speak("playing song")
                webbrowser.open("https://www.youtube.com/watch?v=D9syciL3Xsg")
                pyautogui.sleep(8)  # Give the browser time to open YouTube
                pyautogui.click(1050, 801)  # Click on the search bar (coordinates may vary)
                pyautogui.typewrite(search_query)
                pyautogui.press('enter')
            elif 'play heat' in query:
                speak("playing song")
                webbrowser.open("https://www.youtube.com/watch?v=vAUBe0hMa3w")
                pyautogui.sleep(8)  # Give the browser time to open YouTube
                pyautogui.click(1050, 801)  # Click on the search bar (coordinates may vary)
                pyautogui.typewrite(search_query)
                pyautogui.press('enter')
            elif 'play dance' in query:
                speak("playing song")
                webbrowser.open("https://www.youtube.com/watch?v=vAUBe0hMa3w")
                pyautogui.sleep(8)  # Give the browser time to open YouTube
                pyautogui.click(1050, 801)  # Click on the search bar (coordinates may vary)
                pyautogui.typewrite(search_query)
                pyautogui.press('enter')
            elif 'play way' in query:
                speak("playing song")
                webbrowser.open("https://www.youtube.com/watch?v=fd12oYlbqGQ")
                pyautogui.sleep(8)  # Give the browser time to open YouTube
                pyautogui.click(1050, 801)  # Click on the search bar (coordinates may vary)
                pyautogui.typewrite(search_query)
                pyautogui.press('enter')

# Open brave browser
            elif 'open brave' in query:
                speak("Opening Brave Browser")
                subprocess.Popen(["C:\\Users\\Dell\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"])

            elif 'news' in query:
                speak("Fetching the latest news.")
                news_list = get_news()
                if isinstance(news_list, list):
                    for i, news in enumerate(news_list, 1):
                        speak(f"News {i}: {news}")
                else:
                    speak(news_list)
            
            elif 'search news' in query:
                speak("What topic do you want news about?")
                news_topic = recognize_speech()
                if news_topic != "None":
                    speak(f"Searching news for {news_topic}")
                    news_list = get_news(news_topic)
                    if isinstance(news_list, list):
                        for i, news in enumerate(news_list, 1):
                            speak(f"News {i}: {news}")
                    else:
                        speak(news_list)    

            elif 'wikipedia' in query:
                speak("What would you like to know from Wikipedia?")
                search_query = recognize_speech()
                if search_query != "None":
                    speak(f"Searching Wikipedia for {search_query}")
                    wiki_info = get_wikipedia_info(search_query)
                    speak(wiki_info)
                else:
                    speak("Sorry, I didn't catch that.")   

            elif 'google' in query:
                speak("What do you want to search for on Google?")
                google_query = recognize_speech()
                if google_query != "None":
                    info = get_google_info(google_query)
                    speak(info)            

            elif 'artificial' in query:
                speak("What do you want to ask GPT-3.5?")
                gpt_query = recognize_speech()
                if gpt_query != "None":
                    speak("Querying GPT-3.5")
                    result = query_gpt3(gpt_query)
                    speak(result)           

# Automation using selenium
            elif 'selenium' in query:            # using selenium to automate chrome
                speak("What do you want to search for on Google?")
                search_query = recognize_speech()
                if search_query:
                    speak(f"Searching Google for {search_query}")
                    # Launch the browser and search
                    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                    driver.get("http://www.google.com")
                    search_box = driver.find_element("name", "q")
                    search_box.send_keys(search_query)
                    search_box.send_keys(Keys.RETURN) 
                    time.sleep(20)   #  set time to auto close the window                    

            elif 'exit' in query or 'stop' in query or 'close' in query or 'end' in query or 'sleep' in query or 'stop':
                speak("Goodbye!")
                break
            
            else:
                speak("Sorry, I didn't quite catch that. Could you please repeat or ask something else?")

if __name__ == "__main__":
    jarvis()
