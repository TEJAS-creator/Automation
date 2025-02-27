import pyautogui
import time
import threading
import tkinter as tk

auto_clicking = False

def auto_click(x, y, delay):
    while auto_clicking:
        pyautogui.click(x, y)
        time.sleep(delay)

def start_auto_click():
    global auto_clicking
    auto_clicking = True
    x = int(entry_x.get())
    y = int(entry_y.get())
    delay = float(entry_delay.get())
    threading.Thread(target=auto_click, args=(x, y, delay)).start()

def stop_auto_click():
    global auto_clicking
    auto_clicking = False

# Create the GUI
root = tk.Tk()
root.title("Auto Clicker")

tk.Label(root, text="X Coordinate:").grid(row=0, column=0)
entry_x = tk.Entry(root)
entry_x.grid(row=0, column=1)

tk.Label(root, text="Y Coordinate:").grid(row=1, column=0)
entry_y = tk.Entry(root)
entry_y.grid(row=1, column=1)

tk.Label(root, text="Delay (seconds):").grid(row=2, column=0)
entry_delay = tk.Entry(root)
entry_delay.grid(row=2, column=1)

start_button = tk.Button(root, text="Start", command=start_auto_click)
start_button.grid(row=3, column=0)

stop_button = tk.Button(root, text="Stop", command=stop_auto_click)
stop_button.grid(row=3, column=1)

root.mainloop()
