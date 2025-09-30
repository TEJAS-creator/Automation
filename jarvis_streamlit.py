import datetime
import wikipedia
import streamlit as st

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_topic' not in st.session_state:
    st.session_state.last_topic = None

# Function to get Wikipedia summary
def get_wikipedia_summary(topic: str, sentences=3) -> str:
    topic = topic.strip()
    if not topic:
        return "Please provide a topic for Wikipedia."
    
    try:
        search_results = wikipedia.search(topic)
        if not search_results:
            return f"No Wikipedia results found for '{topic}'."
        
        page_title = search_results[0]
        st.session_state.last_topic = page_title  # save last topic
        return wikipedia.summary(page_title, sentences=sentences)

    except wikipedia.exceptions.DisambiguationError as e:
        options = ', '.join(e.options[:5])
        return f"There are multiple results for '{topic}'. Did you mean: {options}?"

    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{topic}'."

    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Function to process command
def process_command(command: str) -> str:
    command = command.strip().lower()
    
    if not command:
        return "Please type something."

    if "time" in command:
        return datetime.datetime.now().strftime("The time is %I:%M %p")

    elif "date" in command:
        return datetime.datetime.now().strftime("Today is %A, %B %d, %Y")

    elif command in ["more info", "expand", "tell me more"]:
        if st.session_state.last_topic:
            # give 10 sentences for more info
            return get_wikipedia_summary(st.session_state.last_topic, sentences=50)
        else:
            return "No topic to expand. Please ask about a topic first."

    else:
        return get_wikipedia_summary(command)

# Streamlit UI
st.title("📝 Wikipedia Jarvis AI with History")

user_command = st.text_input("Type a topic or command:")
if user_command:
    response = process_command(user_command)
    # Save history
    st.session_state.history.append((user_command, response))

# Display history
for cmd, resp in st.session_state.history:
    st.markdown(f"**You:** {cmd}")
    st.markdown(f"**Jarvis:** {resp}\n")
