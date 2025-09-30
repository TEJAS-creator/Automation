import pyautogui
import time

import subprocess

# Open an application
app_path = r"C:\Path\To\Your\Application.exe"  
subprocess.Popen(app_path)

# Give yourself a few seconds to switch to the target application
print("You have 5 seconds to switch to the target application...")
time.sleep(5)

# Example 1: Automate Mouse Clicks
# Move the mouse to a specific position and click
pyautogui.moveTo(100, 200)  # Move to position (100, 200)
pyautogui.click()           # Perform a mouse click

# Example 2: Automate Keyboard Input
# Type a string
pyautogui.typewrite('Hello, this is an automated message!', interval=0.1)

# Press special keys
pyautogui.press('enter')    # Press the Enter key

# Example 3: Automate Repetitive Task
# Repeat a sequence of actions multiple times
for i in range(5):
    pyautogui.moveTo(100, 200)
    pyautogui.click()
    pyautogui.moveTo(200, 250)
    pyautogui.click()
    pyautogui.typewrite(f'Message {i + 1}', interval=0.1)
    pyautogui.press('enter')
    time.sleep(1)  # Wait for a second before repeating

# Example 4: Taking a Screenshot
screenshot = pyautogui.screenshot()
screenshot.save('screenshot.png')

# Example 5: Finding an Image on the Screen and Clicking It
# (Ensure you have an image file named 'button.png' in the same directory)
button_location = pyautogui.locateOnScreen('button.png')
if button_location:
    button_center = pyautogui.center(button_location)
    pyautogui.click(button_center)
else:
    print("Button not found on the screen.")

print("Automation complete!")
