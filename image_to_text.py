import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64

# Set your Gemini API Key
API_KEY = 'AIzaSyA9UzVlNal1z2PuDQAIsH5Mk0vkHEY1E-U'  # Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)

# Function to generate slide titles
def generate_slide_titles(topic, num_slides):
    """Generates slide titles for the given topic using Gemini."""
    try:
        # Prepare the prompt to generate slide titles
        prompt = f"Generate {num_slides} concise and informative slide titles for the topic '{topic}'."
        
        # Use Gemini model to generate content
        model = genai.GenerativeModel(model_name="models/gemini-pro")  # Adjust the model name as needed
        response = model.generate_content(prompt)
        return response.text.strip().split("\n")
    except Exception as e:
        st.error(f"An error occurred while generating slide titles: {e}")
        return []


# Function to describe an uploaded image
def describe_image(image_bytes, image_format):
    """Generates a description of the uploaded image using Gemini."""
    try:
        # Encode the image to base64
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        
        # Prepare the prompt to describe the image
        prompt = f"Describe this image in detail. Image data: {encoded_image[:300]}..."  # Truncated for brevity
        
        # Use Gemini model to generate content
        model = genai.GenerativeModel(model_name="models/gemini-pro")  # Adjust the model name as needed
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"An error occurred while describing the image: {e}")
        return "Unable to generate image description."


# Streamlit UI
st.title("Slide Title Generator ")
st.sidebar.header("Navigation")
option = st.sidebar.selectbox("Choose an option:", ["Generate Slide Titles", "Describe Image"])

# Slide Title Generation Section
if option == "Generate Slide Titles":
    st.header("Generate Slide Titles")
    topic = st.text_input("Enter the topic:", "")
    num_slides = st.number_input("Enter the number of slides:", min_value=1, max_value=20, value=5)

    if st.button("Generate Titles"):
        if topic.strip() == "":
            st.warning("Please enter a valid topic.")
        else:
            st.write("### Generated Slide Titles:")
            slide_titles = generate_slide_titles(topic, num_slides)
            for idx, title in enumerate(slide_titles, 1):
                st.write(f"{idx}. {title}")

# Image Description Section
if option == "Describe Image":
    st.header("Describe Uploaded Image")
    uploaded_file = st.file_uploader("Upload an image (JPEG/PNG):", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)

            # Get image format and bytes
            image_format = uploaded_file.type.split("/")[-1]
            image_bytes = uploaded_file.getvalue()

            if st.button("Generate Description"):
                description = describe_image(image_bytes, image_format)
                st.write("### Image Description:")
                st.write(description)
        except Exception as e:
            st.error(f"Error processing the image: {e}")
