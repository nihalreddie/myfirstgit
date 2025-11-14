import streamlit as st
from shared_db import get_message as getm
from shared_db import save_message as save

# Page configuration
st.set_page_config(
    page_title="Welcome to CHACHA",
    layout="wide"
)
# jsut to check

def print_hello:
	print("hello")

# Reduce overall font size
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-size: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if 'username' not in st.session_state:
    st.session_state.username = []

if 'password' not in st.session_state:
    st.session_state.password = []

if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True

# Get current user (fallback to Guest if none)
current_user = st.session_state.username[-1] if st.session_state.username else "Guest"

# Display the username
st.write(f"Welcome {current_user}")

# Fetch all stored messages
try:
    messages = getm()
except Exception:
    messages = []

# Render existing chat messages with sender names
if messages:
    for msg in messages:
        if len(msg) >= 2:
            author,text = msg[0], msg[1]
            role = "user" if author == current_user else "assistant"
            with st.chat_message(role):
                st.write(f"**{author}**: {text}")
else:
    st.info("No messages yet. Start the conversation!")

# Chat input for new messages
new_message = st.chat_input("Type your message here (max 200 words)")

if new_message:
    cleaned = new_message.strip()
    if not cleaned:
        st.warning("Please enter a message before sending.")
    else:
        word_count = len(cleaned.split())
        if word_count > 200:
            st.warning(f"Message too long ({word_count} words). Please keep it under 200 words.")
        else:
            sender = current_user if current_user else "Guest"
            save(sender, cleaned)
            with st.chat_message("user"):
                st.write(f"**{sender}**: {cleaned}")
            st.rerun()








