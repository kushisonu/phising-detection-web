import streamlit as st
import google.generativeai as genai
import os
import cred as key

PAGE_TITLE = "AI Powered Phishing Link Scanner"
PAGE_ICON = "🔒"
LAYOUT = "centered"
MODEL_NAME = "gemini-2.0-flash"

API_KEY = key.API_KEY

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

# ✅ Load CSS immediately after setting the page config
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()  # ✅ Call the function to apply custom styles

if not API_KEY:
    st.error(f"API Key not found. Set {API_KEY} as an environment variable.")
    st.stop()

genai.configure(api_key=API_KEY)
# ✅ Chatbot Function
def chatbot_response(query):
    """Fetch chatbot response from Google Gemini AI."""
    
    prompt = f"""
    You are a cybersecurity AI assistant.
    Answer user questions **briefly & accurately** on cybersecurity, phishing, and online safety.

    User Query: {query}
    """

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"


PROMPT_TEMPLATE = """
PROMPT_TEMPLATE = """
PROMPT_TEMPLATE = """
You are an expert cybersecurity analyst specializing in phishing link detection.
Your task is to analyze the following URL and identify potential phishing indicators.
Format the response in **Markdown** to enhance readability.

The URL to analyze is: {url}

Perform the following checks:
- **Typosquatting detection**  
- **HTTPS presence check**  
- **Shortened URL expansion**  
- **Domain age check**  
- **IP Reputation check**  

🔹 **Formatting Instructions:**  
- Use **bold** for section titles.  
- Use `-` for bullet points.  
- Keep responses **concise and structured**.  
- Avoid including **fictional dates or analyst names**
"""


def generate_report(url):
    prompt = PROMPT_TEMPLATE.format(url=url)
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        report = response.text
        return report
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

st.title(PAGE_TITLE)
st.markdown("This tool uses LLMs Google's Genai via Googles generative Model to analyze URLs for potential phishing risks.")
st.markdown("---")

st.markdown("### Enter the URL to check:")
url = st.text_input("URL:")

if st.button("Analyze URL"):
    if url:
        with st.spinner("Analyzing... Please wait."):
            report = generate_report(url)
            if report:
                st.markdown("### Detailed Analysis Report:")
                st.markdown(f"<div style='font-size:18px; line-height:1.6; color: #FFFFFF;'>{report}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a URL.")

st.markdown("---")
st.markdown("<h3 style='text-align: center; color: orange;'>Developed by the code crew 👩‍🦰</h3>",unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Developed with Streamlit | -Powered Phishing Detection</h2>",unsafe_allow_html=True)
# 🔹 Chatbot Section
st.markdown("## 🤖 Chat with AI Security Assistant")
st.markdown("Ask me anything about **cybersecurity, phishing, and online safety**!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("💬 Ask me a question:")
if st.button("Send"):
    if user_input:
        with st.spinner("Thinking..."):
            bot_reply = chatbot_response(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", bot_reply))

# 🔹 Display Chat History
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")

st.markdown("---")

