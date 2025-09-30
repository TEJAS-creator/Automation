import datetime
import wikipedia

# Function to get a robust Wikipedia summary
def get_wikipedia_summary(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        return "Please provide a topic for Wikipedia."
    
    try:
        # First search for the topic to get the closest match
        search_results = wikipedia.search(topic)
        if not search_results:
            return f"No Wikipedia results found for '{topic}'."
        
        # Use the first result for the summary
        page_title = search_results[0]
        summary = wikipedia.summary(page_title, sentences=3)
        return summary

    except wikipedia.exceptions.DisambiguationError as e:
        # Suggest the first 5 options if disambiguation occurs
        options = ', '.join(e.options[:5])
        return f"There are multiple results for '{topic}'. Did you mean: {options}?"

    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{topic}'."

    except Exception as e:
        return f"An unexpected error occurred: {e}"


# Main function to process commands
def process_command(command: str) -> str:
    command = command.strip().lower()
    
    if not command:
        return "Please type something."

    # Return the current time
    if "time" in command:
        return datetime.datetime.now().strftime("The time is %I:%M %p")

    # Return the current date
    elif "date" in command:
        return datetime.datetime.now().strftime("Today is %A, %B %d, %Y")

    # Treat everything else as a Wikipedia query
    else:
        return get_wikipedia_summary(command)
