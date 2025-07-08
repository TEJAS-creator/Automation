# 🐍 Python Automation Scripts

This repository contains a collection of Python scripts designed for various automation tasks, including GUI automation, voice assistance, web scraping, and system operations.

---

## 📜 Scripts Overview

### ⚡ 1. `autoclick.py`
🖱️ A GUI-based auto-clicker that clicks at specified screen coordinates with a user-defined delay.

**Usage:**
- ▶️ Run the script: `python autoclick.py`
- 🎯 Enter X, Y coordinates and delay (in seconds) in the GUI.
- ✅ Click "Start" to begin auto-clicking; "Stop" to halt.

**Dependencies:** `pyautogui`, `tkinter`, `threading`

---

### 📍 2. `coordinates_fast.py`
📌 Prints the current mouse position in real-time to help identify screen coordinates for automation.

**Usage:**
- ▶️ Run the script: `python coordinates_fast.py`
- 🖱️ Move the mouse to see coordinates printed in the console.
- ❌ Stop with `Ctrl+C`.

**Dependencies:** `pyautogui`

---

### 🤖 3. `jarvis.py`
🗣️ A voice-activated virtual assistant that performs tasks like opening applications, controlling media, searching the web, and more.

**Features:**
- 🎤 Responds to voice commands (e.g., "open chrome", "play music").
- 🔍 Integrates with OpenAI GPT-3.5, Wikipedia, News API, and web scraping.
- 🖥️ Controls system functions (e.g., volume, shutdown, screenshots).

**Setup:**
- 🔑 Replace `OPENAI_API_KEY` and `NEWS_API_KEY` with your API keys.
- 🧩 Install ChromeDriver for Selenium-based automation.
- ▶️ Run: `python jarvis.py`
- 🗨️ Say `"jarvis"` followed by a command (e.g., `"jarvis open youtube"`).

**Dependencies:** `speech_recognition`, `pyttsx3`, `pyautogui`, `psutil`, `screen_brightness_control`, `pycaw`, `requests`, `bs4`, `pygetwindow`, `openai`, `wikipedia`, `pywhatkit`, `selenium`, `webdriver_manager`

---

### 💻 4. `os.py`
🧰 Demonstrates various operating system operations using Python's `os` module.

**Features:**
- 🗂️ File and directory manipulation (create, rename, delete).
- 📊 System info (CPU count, process IDs, environment variables).
- 📁 Path operations and directory traversal.

**Usage:**
- ▶️ Run: `python os.py`
- 📤 Outputs results to the console.

**Dependencies:** `os` (built-in)

---

### 🖱️ 5. `pyautogui.py`
🎮 Showcases GUI automation using `pyautogui` for mouse clicks, keyboard input, and screenshots.

**Features:**
- 📌 Automates mouse movements and clicks.
- ⌨️ Types text and presses keys.
- 📷 Captures screenshots and locates images on the screen.

**Usage:**
- 📝 Update `app_path` to the target application.
- 🖼️ Ensure `button.png` exists for image-based clicking.
- ▶️ Run: `python pyautogui.py`

**Dependencies:** `pyautogui`, `subprocess`

---

### ⏰ 6. `schedule.py`
🗓️ A task scheduler that runs functions at specified intervals or times.

**Features:**
- 🔁 Schedules tasks (e.g., every 2 seconds, daily at 10 PM).
- 🧪 Includes examples for periodic and time-specific tasks.

**Usage:**
- ▶️ Run: `python schedule.py`
- ❌ Stop with `Ctrl+C`.

**Dependencies:** `schedule`

---

### 🌐 7. `selenium.py`
🕷️ Demonstrates web automation using Selenium for scraping and interacting with websites.

**Features:**
- 🛒 Scrapes Amazon search results.
- 🔎 Automates Google searches.

**Setup:**
- 🧩 Install ChromeDriver (handled by `webdriver_manager`).
- ▶️ Run: `python selenium.py`

**Dependencies:** `selenium`, `webdriver_manager`

---

### 🗣️ 8. `voice_gemini.py`
🎤 A voice-based chatbot using Google's Gemini API for conversational responses.

**Setup:**
- 🔑 Replace `API_KEY` with your Google API key.
- ▶️ Run: `python voice_gemini.py`
- 🗨️ Speak to interact; say `"bye"` to exit.

**Dependencies:** `google-generativeai`, `speech_recognition`, `pyttsx3`

---

### 🕸️ 9. `web_scrapping.py`
📄 Performs web scraping using `requests` and `BeautifulSoup`, with optional Selenium support for dynamic content.

**Features:**
- 🏷️ Extracts page titles, links, images, and search results.
- 📥 Downloads images and handles pagination.

**Usage:**
- 📝 Modify `url` and class names as needed.
- ▶️ Run: `python web_scrapping.py`
- 💡 Uncomment Selenium code for JavaScript-heavy pages.

**Dependencies:** `requests`, `bs4`, `os`, `csv` (optional: `selenium`)

---

## 📝 Notes

- 🔐 Some scripts (e.g., `jarvis.py`, `voice_gemini.py`) require API keys from OpenAI, News API, and Google.
- 🖥️ Coordinate-based automation may need adjustments for different screen resolutions.
- 🧭 Use `coordinates_fast.py` to find accurate screen coordinates.
- 🧩 Ensure ChromeDriver matches your installed Chrome version for Selenium scripts.

---
