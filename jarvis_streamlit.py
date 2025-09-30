import datetime
import webbrowser
import wikipedia
import requests
from bs4 import BeautifulSoup
import openai

# Your API keys
OPENAI_API_KEY = "Your_API_Key"
openai.api_key = OPENAI_API_KEY
NEWS_API_KEY = "defb8ed0610f4a36ad2c189219fc2773"

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

def get_news(query=None):
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    if query:
        url += f"&q={query}"
    try:
        data = requests.get(url).json()
        return [a['title'] for a in data.get('articles', [])[:5]] or ["No news found."]
    except Exception as e:
        return [f"Error: {e}"]

def process_command(command: str) -> str:
    command = command.lower()

    if "time" in command:
        return datetime.datetime.now().strftime("The time is %I:%M %p")

    elif "date" in command:
        return datetime.datetime.now().strftime("Today is %A, %B %d, %Y")

    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        return wikipedia.summary(topic, sentences=2) if topic else "Give me a topic."

    elif "google" in command:
        topic = command.replace("google", "").strip()
        if topic:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(f"https://www.google.com/search?q={topic}", headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            results = soup.find_all('div', class_='BNeawe')
            return results[0].text if results else "No info found."
        return "What do you want to search?"

    elif "news" in command:
        return "\n".join(get_news())

    elif "youtube" in command and "play" in command:
        song = command.replace("play", "").replace("on youtube", "").strip()
        pywhatkit.playonyt(song)
        return f"Playing {song} on YouTube."

    elif "gpt" in command or "ai" in command:
        return query_gpt3(command)

    elif command in ["exit", "quit", "bye"]:
        return "Goodbye!"

    else:
        return "I didn’t understand that."
