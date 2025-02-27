import google.generativeai as ai
import speech_recognition as sr
import pyttsx3

# API Key
API_KEY = 'Your_API_Key'

# Configure API key
ai.configure(api_key=API_KEY)

# Create a new model
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize speech recognizer
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f'You: {text}')
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Request error from Google Speech Recognition service")
            return ""

# Start a conversation
while True:
    message = listen()
    if message.lower() in ['bye', 'stop', 'exit']:
        print('Chatbot: Goodbye!')
        speak('Goodbye!')
        break
    elif message:
        response = chat.send_message(message)
        print('Chatbot:', response.text)
        speak(response.text)
