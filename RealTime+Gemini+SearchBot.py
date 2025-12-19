import requests
import google.generativeai as genai

# ---------------- CONFIG ----------------
GEMINI_API_KEY = "API_KEY"
GOOGLE_API_KEY = "API_KEY"
CX_ID = "CX_ID"

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

# ---------------- PROMPT ----------------
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

# ---------------- MAIN MENU ----------------
def main():
    print("\n🤖 SMART CHATBOT")
    print("1️⃣ Real-time Search only")
    print("2️⃣ Gemini only")
    print("3️⃣ Real-time Search + Gemini Summary")
    print("Type 'exit' to quit\n")

    while True:
        choice = input("Choose (1/2/3): ")

        if choice.lower() == "exit":
            print("Bye 👋")
            break

        user_query = input("Enter your question: ")

        # -------- 1 --------
        if choice == "1":
            results = google_search(user_query)
            print("\n🔎 Real-time Search Results:\n")
            print(results)

        # -------- 2 --------
        elif choice == "2":
            prompt = build_general_prompt(user_query)
            answer = ask_gemini(prompt)
            print("\n🤖 Gemini Answer:\n")
            print(answer)

        # -------- 3 --------
        elif choice == "3":
            search_data = google_search(user_query)
            prompt = build_general_prompt(user_query, search_data)
            answer = ask_gemini(prompt)

            print("\n🔎 Search Data Used:\n")
            print(search_data)

            print("\n🧠 Gemini Summary:\n")
            print(answer)

        else:
            print("❌ Invalid option. Choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
    
