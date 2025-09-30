import streamlit as st
from jarvis_streamlit import process_command

st.title("📝 Wikipedia Jarvis AI")

user_command = st.text_input("Type a command or topic:")
if user_command:
    response = process_command(user_command)
    st.write(response)
