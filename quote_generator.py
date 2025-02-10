import streamlit as st
import random
import google.generativeai as genai

# Set your Gemini API Key
API_KEY = 'AIzaSyA9UzVlNal1z2PuDQAIsH5Mk0vkHEY1E-U'  # Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)

# Pre-defined list of quotes by categories
quotes_dict = {
    "motivational": [
        "The only way to do great work is to love what you do. – Steve Jobs",
        "Success is not the key to happiness. Happiness is the key to success. – Albert Schweitzer",
        "Your time is limited, so don’t waste it living someone else’s life. – Steve Jobs",
        "It does not matter how slowly you go as long as you do not stop. – Confucius",
        "Success usually comes to those who are too busy to be looking for it. – Henry David Thoreau"
    ],
    "inspirational": [
        "Hardships often prepare ordinary people for an extraordinary destiny. – C.S. Lewis",
        "Everything you can imagine is real. – Pablo Picasso",
        "Believe you can and you're halfway there. – Theodore Roosevelt",
        "The best way to predict the future is to create it. – Peter Drucker",
        "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt"
    ],
    "success": [
        "Success usually comes to those who are too busy to be looking for it. – Henry David Thoreau",
        "Success is not the key to happiness. Happiness is the key to success. – Albert Schweitzer",
        "Success is walking from failure to failure with no loss of enthusiasm. – Winston Churchill",
        "The road to success and the road to failure are almost exactly the same. – Colin R. Davis"
    ]
}

# Function to generate motivational quote using Gemini AI
def generate_motivational_quote(quote_type, topic):
    """Generates a motivational quote based on the quote type and topic using Gemini AI."""
    try:
        # Define the prompt based on user input (quote type and topic)
        prompt = f"Generate a {quote_type} quote on the topic of {topic} to inspire someone to keep going and stay positive."

        # Use Gemini's content generation feature
        model = genai.GenerativeModel(model_name="models/gemini-pro")  # Adjust the model name as needed
        response = model.generate_content(prompt)

        # Extract generated quote from the response
        quote = response.text.strip()
        return quote
    except Exception as e:
        st.error(f"An error occurred while generating the quote: {e}")
        return None

def main():
    """Main function to handle user input and generate a motivational quote."""
    st.title("Motivational Quote Bot")

    # Ask the user what type of quote they want
    quote_type = st.selectbox(
        "Select the type of quote you'd like to hear:",
        ["motivational", "inspirational", "success"]
    )

    # Ask the user for the topic
    topic = st.text_input("Enter the topic you'd like the quote to be about (e.g., work, life, success):")

    # Button to trigger quote generation
    generate_button = st.button("Get Quote")

    if generate_button and topic:
        st.info("Generating quote... Please wait.")
        
        # Randomly select a quote from the predefined list or use Gemini AI model
        if random.choice([True, False]):
            # Select from pre-defined list of quotes
            quote = random.choice(quotes_dict[quote_type])
        else:
            # Generate quote using Gemini AI model with the provided topic
            quote = generate_motivational_quote(quote_type, topic)

        if quote:
            # Display the generated or selected quote
            st.write(f"### {quote_type.capitalize()} Quote on '{topic.capitalize()}':")
            st.write(f"**{quote}**")

if __name__ == "__main__":
    main()
