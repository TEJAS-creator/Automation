# Google blocks automated scraping – Their pages rely heavily on JavaScript, and they prevent direct scraping.
# The page is not fully loaded in requests – Many elements are loaded dynamically.
# Your class names are wrong – Google doesn’t use static class names (they change frequently).
# Use Selenium instead of BeautifulSoup alone (Google uses JavaScript).


import requests
from bs4 import BeautifulSoup
import os
import csv
# Uncomment below if using Selenium for dynamic content scraping
# from selenium import webdriver  

# URL to scrape
url = "https://www.google.com/"
# Fetch the webpage
response = requests.get(url)
response.raise_for_status()  # Ensure request was successful

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# 1. Extract and print the page title
print("Page Title:", soup.title.text)

# 2. Extract the first <h1> tag
h1_tag = soup.find("h1")
print("First H1:", h1_tag.text if h1_tag else "No H1 tag found")

# 3. Extract all links from the page
print("\nAll Links:")
for link in soup.find_all("a"):
    print(link.get("href"))

# 4. Extract a section by class name (Modify class name as per website)
section = soup.find("div", class_="some-class-name")
print("\nSection Content:", section.text if section else "No matching section found")

# 5. Extract a specific element by ID
element = soup.find(id="unique-id")
print("\nElement by ID:", element.text if element else "No element with given ID found")

# 6. Extract all table rows
table = soup.find("table")
if table:
    print("\nTable Data:")
    rows = table.find_all("tr")
    for row in rows:
        print(row.text.strip())

# 7. Extract all list items
print("\nList Items:")
for item in soup.find_all("li"):
    print(item.text)

# 8. Extract all image URLs
print("\nImage URLs:")
for img in soup.find_all("img"):
    print(img["src"])

# 9. Scrape multiple pages (pagination example)
for page in range(1, 3):  # Scraping first 2 pages as an example
    paginated_url = f"https://example.com/page/{page}"
    paginated_response = requests.get(paginated_url)
    paginated_soup = BeautifulSoup(paginated_response.content, "html.parser")
    print(f"\nScraping Page {page}...")

# 10. Download images from the website
os.makedirs("images", exist_ok=True)
for i, img in enumerate(soup.find_all("img")):
    img_url = img["src"]
    img_data = requests.get(img_url).content
    with open(f"images/image_{i}.jpg", "wb") as file:
        file.write(img_data)

# 11. Automate Google Search Results Scraping
search_query = "anime"
google_url = f"https://www.google.com/search?q={search_query}"
headers = {"User-Agent": "Mozilla/5.0"}
google_response = requests.get(google_url, headers=headers)
google_soup = BeautifulSoup(google_response.content, "html.parser")

print("\nGoogle Search Results Titles:")
for result in google_soup.find_all("h3"):
    print(result.text)

# 12. Web Scraping using Selenium (for JavaScript-heavy pages)
# driver = webdriver.Chrome()  
# driver.get("https://www.example.com")  
# html = driver.page_source  
# selenium_soup = BeautifulSoup(html, "html.parser")  
# print("\nSelenium Scraped Content:")
# print(selenium_soup.prettify())
# driver.quit()

print("Task finished")
