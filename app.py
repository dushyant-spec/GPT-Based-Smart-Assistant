import streamlit as st
from openai import OpenAI
import os
import speech_recognition as sr
import pyttsx3
import webbrowser

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------------- Existing Code ----------------
Model = "gpt-4o-mini"
client = OpenAI(api_key=OPENAI_API_KEY)
def Reply(question):
    completion = client.chat.completions.create(
        model=Model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question}
        ],
        max_tokens=200
    )
    answer = completion.choices[0].message.content
    return answer

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommend():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        st.write("🧠 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        st.success(f"✅ You said: {query}")
    except Exception as e:
        st.error("❌ Say that again...")
        return "None"
    return query

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Voice Assistant", page_icon="🎧", layout="centered")
st.title("🎙️ Voice Assistant with OpenAI + Streamlit")

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

start_btn = st.button("🎤 Start Listening")

if start_btn:
    query = takeCommend().lower()
    if query != "none":
        ans = Reply(query)
        st.session_state.chat_log.append(("You", query))
        st.session_state.chat_log.append(("Assistant", ans))
        st.write(f"🤖 **Assistant:** {ans}")
        speak(ans)

        # Browser commands
        if "open youtube" in query:
            webbrowser.open('https://www.youtube.com')
        if "open google" in query:
            webbrowser.open('https://www.google.com')
        if "bye" in query:
            st.warning("👋 Assistant stopped.")

# Display chat log
st.markdown("---")
st.subheader("📝 Conversation Log")
for speaker, text in st.session_state.chat_log:
    if speaker == "You":
        st.markdown(f"🧑 **{speaker}:** {text}")
    else:
        st.markdown(f"🤖 **{speaker}:** {text}")
