import streamlit as st
from jarvis_streamlit import process_command  # import your function

st.set_page_config(page_title="Jarvis AI Assistant", page_icon="🤖")

st.title("🤖 Jarvis AI Assistant")
st.write("Type a command and let Jarvis respond!")

# Input box
user_command = st.text_input("Your command:")

if st.button("Run"):
    if user_command.strip():
        response = process_command(user_command)
        st.success(f"Jarvis: {response}")
    else:
        st.warning("Please enter a command.")
