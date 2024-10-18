import os
from groq import Groq
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
os.environ["GROQ_API_KEY"] = api_key

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "prev_subject" not in st.session_state:
    st.session_state.prev_subject = ""

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

sname = st.sidebar.text_input("Subject : ")
level = st.sidebar.selectbox("Level : ", ("Novice", "Intermediate", "Expert"))
a = st.sidebar.text_input("Question : ")

if sname != st.session_state.prev_subject:
    st.session_state.chat_history = []
    st.session_state.prev_subject = sname

if st.session_state.chat_history:
    st.write("### Chat History")
    for entry in st.session_state.chat_history:
        st.write(f"**User:** {entry['user']}")
        st.write(f"**AI:** {entry['ai']}")
else:
    st.write("Start messaging")

if st.sidebar.button("Submit"):
    if a:

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "You are a expert in " + sname + " and the level of answer generated should be " + level + " you have to reply as best you could and the answer should not exceed more than 200 words" + a
                }
            ],
            model="llama3-8b-8192",
        )
        ai_response = chat_completion.choices[0].message.content
        st.session_state.chat_history.append({"user": a, "ai": ai_response})

        st.write("### AI Response")
        st.write(ai_response)

        st.write("### Chat History")
        for entry in st.session_state.chat_history:
            st.write(f"**User:** {entry['user']}")
            st.write(f"**AI:** {entry['ai']}")

    else:
        st.write("Please enter a prompt")

