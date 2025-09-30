import datetime
import wikipedia
import requests
from bs4 import BeautifulSoup
import openai

# Your API keys
OPENAI_API_KEY = "Your_API_Key"
openai.api_key = OPENAI_API_KEY
NEWS_API_KEY = "defb8ed0610f4a36ad2c189219fc2773"


def get_wikipedia_summary(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        return "Please provide a topic for Wikipedia."
    
    try:
        return wikipedia.summary(topic, sentences=3)
    except wikipedia.exceptions.DisambiguationError as e:
        options = ', '.join(e.options[:5])  # show first 5 options
        return f"There are multiple results for '{topic}'. Did you mean: {options}?"
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{topic}'."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def get_google_info(query: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='BNeawe')
        if results:
            return "\n".join([res.text for res in results[:5]])
        return "No results found."
    except Exception as e:
        return f"Error: {e}"


def query_gpt3(query: str) -> str:
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


def get_news(query=None) -> list:
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
        return get_wikipedia_summary(topic)

    elif "google" in command:
        search_query = command.replace("google", "").strip()
        if search_query:
            return get_google_info(search_query)
        else:
            return "Please provide a search term after 'google'. Example: google Python programming"

    elif "news" in command:
        return "\n".join(get_news())

    elif "gpt" in command or "ai" in command:
        return query_gpt3(command)

    elif command in ["exit", "quit", "bye"]:
        return "Goodbye!"

    else:
        return "I didn’t understand that."
