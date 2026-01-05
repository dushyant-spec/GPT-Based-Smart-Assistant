import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Smart Assistant", page_icon="🤖")
st.title("🤖 GPT-Based Smart Assistant")

# ✅ Correct way to load API key on Streamlit Cloud
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

query = st.text_input("💬 Ask me anything")

if st.button("Send") and query:
    answer = reply(query)
    st.session_state.chat_log.append(("You", query))
    st.session_state.chat_log.append(("Assistant", answer))

st.markdown("---")
for role, text in st.session_state.chat_log:
    st.markdown(f"**{role}:** {text}")
