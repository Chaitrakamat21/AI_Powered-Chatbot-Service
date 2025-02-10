import requests
import streamlit as st
import base64
import google.generativeai as genai  # Ensure the genai library is installed
from google.generativeai import GenerativeModel

# API keys for Hugging Face and Google Gemini
HUGGING_FACE_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyA9UzVlNal1z2PuDQAIsH5Mk0vkHEY1E-U"

# API endpoints
TEXT_TO_IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

# Authentication headers for Hugging Face
hugging_face_headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
}

# Configure the Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def generate_image_from_text(prompt):
    """
    Generates an image from a text prompt using Hugging Face's Stable Diffusion API.

    Args:
        prompt (str): The text prompt to generate the image.

    Returns:
        bytes: The generated image as a byte stream.
    """
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    response = requests.post(TEXT_TO_IMAGE_API_URL, headers=hugging_face_headers, json=payload)

    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

def generate_hashtags_from_prompt(prompt):
    """
    Generates hashtags for a given prompt using the Google Gemini API.

    Args:
        prompt (str): The text prompt to generate hashtags from.

    Returns:
        str: The generated hashtags.
    """
    try:
        # Initialize the model for content generation
        model = GenerativeModel(model_name="models/gemini-pro")

        # Create the prompt for generating hashtags
        hashtags_prompt = f"Generate hashtags for the following content: '{prompt}'"
        response = model.generate_content(hashtags_prompt)

        hashtags = response.text.strip()
        return hashtags
    except Exception as e:
        st.error(f"An error occurred while generating hashtags: {e}")
        return None

def create_download_link(content, filename="hashtags.txt"):
    """
    Generates a download link for the provided content.

    Args:
        content (str): The content to be downloaded.
        filename (str): The name of the file to download.

    Returns:
        str: A URL to download the content.
    """
    b64_content = base64.b64encode(content.encode()).decode()  # Encode the content to base64
    return f"data:file/txt;base64,{b64_content}"

def main():
    st.title("hashtag generator")
    st.markdown("""
        Generate beautiful images and suggested hashtags for your social media posts using Hugging Face's Stable Diffusion and the Google Gemini API.
    """)

    # Input field for text prompt
    prompt = st.text_input("Enter your prompt:", "A futuristic cityscape with flying cars at sunset")

    if st.button("Generate Post"):
        if prompt.strip():
            with st.spinner("Generating image and hashtags..."):
                # Generate the image from the text prompt
                image_data = generate_image_from_text(prompt)
                if image_data:
                    st.image(image_data, caption="Generated Image", use_column_width=True)

                # Generate hashtags for the text prompt
                hashtags = generate_hashtags_from_prompt(prompt)
                if hashtags:
                    st.subheader("Suggested Hashtags")
                    st.write(hashtags)
                    # Provide a download link for the hashtags
                    download_url = create_download_link(hashtags)
                    st.markdown(f"[Download Hashtags]({download_url})")
        else:
            st.warning("Please enter a text prompt to generate the post.")

if __name__ == "__main__":
    main()
