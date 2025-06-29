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

# 🚨 Critical phrases that indicate crisis
crisis_keywords = [
    "i want to die", "i don't want to live", "kill myself", "end my life", "end it all", 
    "jump from", "fall from", "want to fall", "want to jump", "hurt myself", 
    "i want to end it", "suicidal", "take my life", "life is meaningless"
]

# 😔 Negative emotional expressions
negative_keywords = [
    "cry", "crying", "cried", "not ok", "not okay", "not fine", "i am sad", "depressed", 
    "tense", "worried", "anxious", "scared", "fear", "afraid", "panicking", 
    "broken", "feel low", "helpless", "overwhelmed", "alone", "i hate this", 
    "frustrated", "angry", "irritated", "i feel down", "hopeless", "i am scared", 
    "lost", "worthless", "lonely"
]

# 😊 Positive emotional expressions
positive_keywords = [
    "happy", "celebrate", "excited", "dancing", "topper", "won", "yay", "enjoy",
    "smiling", "ice cream", "icecream", "chocolate", "relaxed", "proud", "calm", 
    "peaceful", "joyful", "feeling great", "got a job", "promotion", "rank", 
    "satisfied", "loved", "grateful", "content", "motivated"
]

def get_bot_reply(user_message):
    text = user_message.lower()
    score = analyzer.polarity_scores(text)
    compound = score['compound']

    def keyword_match(keywords):
        return any(keyword in text for keyword in keywords)

    # Crisis check
    if keyword_match(crisis_keywords):
        mood = "🚨 Urgent"
        reply = (
            "I'm really concerned about what you're feeling. You're **not alone** 💙\n\n"
            "Please consider reaching out to a friend, a counselor, or a mental health professional.\n"
            "You are **valuable** and your life matters deeply. 🫂"
        )
    elif keyword_match(negative_keywords):
        mood = "😔 Negative"
        reply = "I'm really sorry you're feeling this way. You're not alone, and I'm here for you 💙"
    elif keyword_match(positive_keywords):
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

# Chat UI
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Type your message:")
    submit = st.form_submit_button("Send")

    if submit and user_input:
        st.session_state.chat.append(("You", user_input))
        bot_response = get_bot_reply(user_input)
        st.session_state.chat.append(("EmpaBot", bot_response))

# Show messages
for sender, message in st.session_state.chat:
    if sender == "You":
        st.markdown(f"🧍 **{sender}:** {message}")
    else:
        st.markdown(f"🤖 **{sender}:** {message}")

# Feedback line
st.markdown("---")
st.markdown("📝 *If something doesn’t feel right or if you’d like to improve me, feel free to share your suggestions!*")
