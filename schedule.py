import schedule
import time

def say_hello():
    print("Hello, world!")

def say_goodbye():
    print("Goodbye, world!")

def remind():
    print("Reminder: Stay focused!")

def greet_morning():
    print("Good morning! Have a great day!")

def greet_night():
    print("Good night! Sleep well!")

# Schedule tasks
schedule.every(2).seconds.do(say_hello)       # Every 2 seconds
schedule.every(5).seconds.do(say_goodbye)     # Every 5 seconds
schedule.every().minute.do(remind)            # Every minute
schedule.every().hour.do(greet_morning)       # Every hour
schedule.every().day.at("22:00").do(greet_night)  # Every day at 10 PM
schedule.every().monday.do(lambda: print("Happy Monday!"))  # Every Monday
schedule.every().wednesday.at("15:30").do(lambda: print("It's Wednesday 3:30 PM!"))  # Specific time

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
