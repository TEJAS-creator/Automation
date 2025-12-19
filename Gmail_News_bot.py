import requests
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------- CONFIG ----------------
GEMINI_API_KEY = "api"
GOOGLE_API_KEY = "api"
CX_ID = "key_id"

SENDER_EMAIL = "sender@gmail.com"
APP_PASSWORD = "16 digit code "
RECEIVER_EMAIL = "receiver@gmail.com"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- GOOGLE SEARCH ----------------
def google_search(query, num_results=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": CX_ID,
        "q": query,
        "num": num_results
    }

    res = requests.get(url, params=params)
    data = res.json()

    if "items" not in data:
        return "No search results found."

    snippets = []
    for item in data["items"]:
        snippets.append(f"- {item['title']}: {item['snippet']}")

    return "\n".join(snippets)

# ---------------- PROMPT BUILDER ----------------
def build_general_prompt(user_query, context=""):
    return f"""
You are a highly intelligent, reliable AI assistant.

Guidelines:
- Answer clearly and concisely
- Use provided context if available
- Do NOT hallucinate
- If unsure, say so

Context:
{context}

User Question:
{user_query}
"""

# ---------------- GEMINI ----------------
def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# ---------------- NEWS + EMAIL ----------------
def generate_news_and_send_email():
    prompt = """
Give me top 10 latest news in each of the following genres:
1. Technology
2. Indian Politics
3. Sports
4. Finance
5. Stock Market
6. Lifestyle

Requirements:
- Each category should have exactly 10 crisp bullet points.
- Keep points short (maximum 1 sentence).
- Do NOT add extra text like introductions or summaries.
- Format:

### <Category Name>
1. ...
2. ...
...
10. ...
"""

    response = model.generate_content(prompt)
    news_text = response.text

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "📰 Today's News Summary"

    msg.attach(MIMEText(news_text, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("\n✅ News email sent successfully!\n")

    except Exception as e:
        print("\n❌ Failed to send email:", e)

# ---------------- MAIN MENU ----------------
def main():
    print("\n🤖 SMART CHATBOT")
    print("1️⃣ Real-time Search only")
    print("2️⃣ Gemini only")
    print("3️⃣ Real-time Search + Gemini Summary")
    print("4️⃣ Daily News + Send Email")
    print("Type 'exit' to quit\n")

    while True:
        choice = input("Choose (1/2/3/4): ")

        if choice.lower() == "exit":
            print("Bye 👋")
            break

        # -------- OPTION 1 --------
        if choice == "1":
            user_query = input("Enter your question: ")
            results = google_search(user_query)
            print("\n🔎 Real-time Search Results:\n")
            print(results)

        # -------- OPTION 2 --------
        elif choice == "2":
            user_query = input("Enter your question: ")
            prompt = build_general_prompt(user_query)
            answer = ask_gemini(prompt)
            print("\n🤖 Gemini Answer:\n")
            print(answer)

        # -------- OPTION 3 --------
        elif choice == "3":
            user_query = input("Enter your question: ")
            search_data = google_search(user_query)
            prompt = build_general_prompt(user_query, search_data)
            answer = ask_gemini(prompt)

            print("\n🔎 Search Data Used:\n")
            print(search_data)

            print("\n🧠 Gemini Summary:\n")
            print(answer)

        # -------- OPTION 4 --------
        elif choice == "4":
            generate_news_and_send_email()

        else:
            print("❌ Invalid option. Choose 1, 2, 3, or 4.")

# ---------------- RUN ----------------
if __name__ == "__main__":
    main()













