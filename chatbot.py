import google.generativeai as genai
import streamlit as st

# Set your API key
genai.configure(api_key="AIzaSyA9UzVlNal1z2PuDQAIsH5Mk0vkHEY1E-U")  # Replace YOUR_API_KEY with your actual API key

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get chatbot response
def chat_with_gpt(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit app setup
st.title("Chatbot with Google Gemini")
st.write("Type your message below and press 'Send'.")

user_input = st.text_input("You: ")
if st.button("Send"):
    if user_input:
        bot_response = chat_with_gpt(user_input)
        st.text_area("Bot:", value=bot_response, height=200)
