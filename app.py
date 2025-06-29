import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="EmpaBot – Mental Health Chatbot", page_icon="💬")

st.title("💬 EmpaBot – Your Mental Wellness Companion")
st.markdown("Hi there! I'm here to listen. How are you feeling today?")

# Store chat history
if 'chat' not in st.session_state:
    st.session_state.chat = []

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# Smart keyword matching
def get_bot_reply(user_message):
    text = user_message.lower()
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']

    # Enhanced manual emotion detection
    if any(word in text for word in ['cry', 'failed', 'oh no', 'stress', 'tension', 'nervous', 'worry', 'scare']):
        mood = "😔 Negative"
        reply = "I'm really sorry you're feeling this way. You're not alone, and I'm here for you 💙"
    elif any(word in text for word in ['rank', 'topper', 'dance', 'enjoy', 'yay', 'won', 'celebrate']):
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
