import streamlit as st
import google.generativeai as genai
import base64

# Configure the Gemini API key (replace with your actual Gemini API key)
API_KEY = "AIzaSyA9UzVlNal1z2PuDQAIsH5Mk0vkHEY1E-U"  # Replace with your actual key
genai.configure(api_key=API_KEY)

def generate_blog_content(topic):
    """Generates blog title and content using Gemini."""
    try:
        # List available models (for debugging and finding correct model name)
        # models = [m.name for m in genai.list_models()]
        # st.write("Available Models:", models) # Uncomment to see available models

        # Use a valid model name. Find the model name by uncommenting the above lines
        model = genai.GenerativeModel(model_name="models/gemini-pro")  # or models/gemini-pro-vision

        # Generate blog title
        title_prompt = f"Generate an engaging blog title for the topic: '{topic}'"
        title_response = model.generate_content(title_prompt)
        title = title_response.text.strip()

        # Generate blog content
        content_prompt = f"Write a detailed blog post about '{topic}' with the title: '{title}'"
        content_response = model.generate_content(content_prompt)
        content = content_response.text.strip()

        return title, content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

def download_link(content, filename="blog_post.txt"):
    """Generates a download link for the content."""
    b64_content = base64.b64encode(content.encode()).decode()  # Encode the content to base64
    download_url = f"data:file/txt;base64,{b64_content}"
    return download_url

def main():
    """Streamlit main function to run the app."""
    st.title("Blog Post Generator with Gemini API")

    topic = st.text_input("Enter a topic for your blog:")
    if topic:
        st.write(f"Generating content for: {topic}...")
        
        # Generate blog content
        title, content = generate_blog_content(topic)

        if title and content:
            st.subheader("Generated Blog Title:")
            st.write(title)
            
            st.subheader("Generated Blog Content:")
            st.write(content)
            
            # Provide a download link for the blog content
            download_url = download_link(content)
            st.markdown(f"[Download Blog Post]( {download_url} )", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
