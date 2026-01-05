import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Smart Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 GPT-Based Smart Assistant")
st.caption("Cloud-native • Stable • Deployable")

# Initialize chat history
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

def reply(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question}
        ],
        max_tokens=200
    )
    return response.choices[0].message.content

# UI
query = st.text_input("💬 Ask me anything")

if st.button("Send") and query:
    answer = reply(query)
    st.session_state.chat_log.append(("You", query))
    st.session_state.chat_log.append(("Assistant", answer))

# Display chat
st.markdown("---")
for role, text in st.session_state.chat_log:
    if role == "You":
        st.markdown(f"🧑 **You:** {text}")
    else:
        st.markdown(f"🤖 **Assistant:** {text}")
