import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------------------
# CONFIGURE GEMINI API KEY
# ---------------------------
API_KEY = "api key"
genai.configure(api_key=API_KEY)

# ---------------------------
# PROMPT CONTENT
# ---------------------------
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

### <Next Category>
...
"""

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(prompt)
news_text = response.text

# ---------------------------
# EMAIL CONFIG
# ---------------------------
sender_email = "sender@gmail.com"
app_password = "16 digit password "
receiver_email = "receiver@gmail.com"

subject = "Today's News Summary"

# Create Email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

msg.attach(MIMEText(news_text, 'plain'))

# ---------------------------
# SEND EMAIL USING GMAIL SMTP
# ---------------------------
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully!")

except Exception as e:
    print("Failed to send email:", e)
