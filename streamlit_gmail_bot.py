import streamlit as st
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- STREAMLIT UI SETTINGS ---
st.set_page_config(page_title="News Email Sender", layout="centered")
st.title("📰 News Generator & Email Sender")

# --- INPUT FIELDS ---
sender_email = st.text_input("Sender Email", "")
app_password = st.text_input("App Password", type="password")
receiver_email = st.text_input("Receiver Email", "")

default_prompt = """
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

### <Next Category>
...
"""

prompt = st.text_area("Prompt", value=default_prompt, height=300)

api_key = st.text_input("Gemini API Key", type="password")

# --- GENERATE NEWS BUTTON ---
generate_btn = st.button("Generate News", type="primary")  # Blue button

news_text = ""

if generate_btn:
    if api_key.strip() == "":
        st.error("Please enter your Gemini API key!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            news_text = response.text

            st.success("News generated successfully!")
            st.text_area("Generated News", value=news_text, height=400)

        except Exception as e:
            st.error(f"Error generating news: {e}")

# --- SEND EMAIL BUTTON ---
if "news_text" not in st.session_state:
    st.session_state.news_text = ""

if generate_btn:
    st.session_state.news_text = news_text

send_btn = st.button("Send Email", help="Send the generated news via Gmail",
                     key="send", on_click=None)

if send_btn:
    if not sender_email or not app_password or not receiver_email:
        st.error("Please fill all email fields!")
    elif st.session_state.news_text.strip() == "":
        st.error("No news generated to send!")
    else:
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "Today's News Summary"
            msg.attach(MIMEText(st.session_state.news_text, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()

            st.success("Email sent successfully!")

        except Exception as e:
            st.error(f"Failed to send email: {e}")
