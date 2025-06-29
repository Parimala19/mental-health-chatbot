import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="EmpaBot – Mental Health Chatbot", page_icon="💬")

st.title("💬 EmpaBot – Your Mental Wellness Companion")
st.markdown("Hi there! I'm here to listen. How are you feeling today?")

# Store chat history
if 'chat' not in st.session_state:
    st.session_state.chat = []

# Initialize analyzer
analyzer = SentimentIntensityAnalyzer()

# Keywords
crisis_keywords = ["i want to die", "i don't want to live", "suicidal", "kill myself", "end it all"]
negative_keywords = [
    "cry", "crying", "cried", "want to cry", "not ok", "not okay", "not fine", "sad", "depressed",
    "tension", "worried", "anxious", "stressed", "scared", "panicking", "i am broken",
    "i feel low", "helpless", "overwhelmed", "alone", "i hate this", "afraid", "fear"
]
positive_keywords = [
    "happy", "celebrate", "excited", "dancing", "rank", "topper", "won", "yay", "enjoy",
    "smiling", "ice cream", "icecream", "chocolate", "relaxed", "proud", "calm", "peaceful",
    "joyful", "feeling great"
]

def get_bot_reply(user_message):
    text = user_message.lower()
    compound = analyzer.polarity_scores(text)['compound']

    def keyword_in(keywords):
        return any(kw in text for kw in keywords)

    # 🚨 Crisis check
    if keyword_in(crisis_keywords):
        mood = "🚨 Urgent"
        reply = ("I'm really concerned about what you're feeling. You're **not alone**. 💙 "
                 "Please consider talking to a friend, a trusted adult, or calling a mental health helpline. "
                 "**You matter.**")
    elif keyword_in(negative_keywords):
        mood = "😔 Negative"
        reply = "I'm really sorry you're feeling this way. You're not alone, and I'm here for you 💙"
    elif keyword_in(positive_keywords):
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

# Chat input form
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Type your message:")
    submit = st.form_submit_button("Send")

    if submit and user_input:
        st.session_state.chat.append(("You", user_input))
        bot_response = get_bot_reply(user_input)
        st.session_state.chat.append(("EmpaBot", bot_response))

# Show conversation
for sender, message in st.session_state.chat:
    if sender == "You":
        st.markdown(f"🧍 **{sender}:** {message}")
    else:
        st.markdown(f"🤖 **{sender}:** {message}")

# Footer note
st.markdown("---")
st.markdown("⚠️ *If my response didn't feel accurate, please share feedback. I'm learning to understand human emotions better.*")
