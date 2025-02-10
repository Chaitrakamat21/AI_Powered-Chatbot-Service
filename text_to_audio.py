import requests
import streamlit as st

# Your Hugging Face API key
API_KEY = "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"

# API endpoint for text-to-audio generation
API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def text_to_audio(prompt):
    """
    Generate audio from a text prompt using Hugging Face API.

    Args:
        prompt (str): The text prompt for generating the audio.

    Returns:
        bytes: The generated audio data in WAV format.
    """
    # Payload with the text prompt
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    # Make a POST request to the API
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Failed to generate audio. Status code: {response.status_code}, Error: {response.text}")
        return None

# Streamlit frontend
def main():
    st.title("Text-to-Audio Generator")
    st.markdown("Generate realistic audio from your text prompts using Hugging Face's Text-to-Speech API.")

    # Input text prompt
    prompt = st.text_input("Enter your text prompt:", "Hello, welcome to the future of text-to-speech technology!")

    if st.button("Generate Audio"):
        if prompt.strip():
            with st.spinner("Generating audio..."):
                audio_data = text_to_audio(prompt)
                if audio_data:
                    st.audio(audio_data, format="audio/wav")
        else:
            st.warning("Please enter a text prompt.")

if __name__ == "__main__":
    main()
