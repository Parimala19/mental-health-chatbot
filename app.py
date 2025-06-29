import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

st.set_page_config(page_title="EmpaBot – Mental Health Chatbot", page_icon="💬")

st.title("💬 EmpaBot – Your Mental Wellness Companion")
st.markdown("Hi there! I'm here to listen. How are you feeling today?")

# Store chat history
if 'chat' not in st.session_state:
    st.session_state.chat = []

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# Emotion keyword patterns
negative_patterns = ['cry', 'fail', 'oh no', 'stress', 'tension', 'nervous', 'worry', 'scare']
positive_patterns = ['rank', 'topper', 'dance', 'enjoy', 'yay', 'won', 'celebrate', 'happy']

def get_bot_reply(user_message):
    text = user_message.lower()
    compound = analyzer.polarity_scores(text)['compound']

    # Keyword pattern matching
    def match_any(patterns):
        return any(re.search(rf"\b{pattern}\w*\b", text) for pattern in patterns)

    if match_any(negative_patterns):
        mood = "😔 Negative"
        reply = "I'm really sorry you're feeling this way. You're not alone, and I'm here for you 💙"
    elif match_any(positive_patterns):
        mood = "😊 Positive"
        reply = "That's amazing! I'm so happy for you! Keep it up and celebrate your wins 🎉"
    elif compound >= 0.3:
        mood = "😊 Positive"
        reply = "I'm so glad you're feeling good! Keep spreading the positivity 💫"
    elif compound <= -0.3:
        mood = "😔 Negative"
        reply = "I'm really sorry you're feeling this way. You're not alone, and I'm here for you 💙"
    else:
        mood = "😐 Neutral"
        reply = "Thank you for sharing. I'm here to listen and support you however I can."

    return f"{reply}\n\n**(Detected Mood: {mood})**"

# Chat input area
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Type your message:")
    submit = st.form_submit_button("Send")

    if submit and user_input:
        st.session_state.chat.append(("You", user_input))
        bot_response = get_bot_reply(user_input)
        st.session_state.chat.append(("EmpaBot", bot_response))

# Display chat
for sender, message in st.session_state.chat:
    if sender == "You":
        st.markdown(f"🧍 **{sender}:** {message}")
    else:
        st.markdown(f"🤖 **{sender}:** {message}")
