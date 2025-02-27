from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
query= "mobiles"
driver.get(f"https://www.amazon.in/s?k={query}&crid=IIMDIGPUZERE&sprefix=mobile%2Caps%2C301&ref=nb_sb_noss_1")

elem= driver.find_element(By.CLASS_NAME,"puis-card-container")
print(elem.text)

time.sleep(5)
driver.close()

# CODE 2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open Google
driver.get("https://www.google.com")

time.sleep(2)  # Wait for the page to load

# Find the search bar using its name attribute
elem = driver.find_element(By.NAME, "q")
elem.click()  # Click on the search bar
time.sleep(5)  # Wait to see the effect before closing the browser
driver.close()
