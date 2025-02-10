import streamlit as st
import google.generativeai as genai

# Set your Gemini API Key
API_KEY = 'AIzaSyA9UzVlNal1z2PuDQAIsH5Mk0vkHEY1E-U'  # Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)

# List of supported languages (including major Indian languages)
languages = [
    "English", "Spanish", "French", "German", "Italian", "Hindi",  
    "Chinese", "Japanese", "Russian", "Portuguese", "Arabic", 
    "Korean", "Dutch", "Turkish", "Swedish", "Polish", "Thai", 
    "Greek", "Czech", "Hungarian", "Romanian", "Bengali", "Telugu", 
    "Tamil", "Urdu", "Gujarati", "Malayalam", "Kannada", "Punjabi", 
    "Odia", "Maithili", "Assamese", "Sanskrit", "Marathi", "Rajasthani", 
    "Konkani", "Sindhi", "Dogri", "Kashmiri", "Nepali"
]

def translate_text(input_text, source_lang, target_lang):
    """Translate text using Gemini AI."""
    try:
        # Formulate the prompt for translation
        prompt = f"Translate the following text from {source_lang} to {target_lang}: {input_text}"

        # Use Gemini's content generation feature
        model = genai.GenerativeModel(model_name="models/gemini-pro")  # Adjust the model name as needed
        response = model.generate_content(prompt)

        # Extract translated text from the response
        translated_text = response.text.strip()
        return translated_text
    except Exception as e:
        st.error(f"An error occurred while translating: {e}")
        return None

def main():
    """Main function to handle user input and translation."""
    st.title("Language Translation Bot")

    # Select source and target languages
    source_lang = st.selectbox("Select the source language", languages)
    target_lang = st.selectbox("Select the target language", languages)

    # Input field for text to translate
    input_text = st.text_area("Enter text to translate:")

    # Button to trigger translation
    translate_button = st.button("Translate")

    if translate_button and input_text:
        st.info("Translating... Please wait.")
        
        # Translate the input text
        translated_text = translate_text(input_text, source_lang, target_lang)

        if translated_text:
            # Display the translated text
            st.write(f"### Translated Text ({source_lang} to {target_lang}):")
            st.write(translated_text)

if __name__ == "__main__":
    main()
