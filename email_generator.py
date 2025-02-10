import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

# Configure Gemini API Key (replace with your actual Gemini API key)
API_KEY = 'AIzaSyA9UzVlNal1z2PuDQAIsH5Mk0vkHEY1E-U'  # Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)

# Function to get email content from Gemini (updated for Gemini model)
def generate_email_content(reason, details):
    prompt = f"Write a professional email for the following reason: {reason}. The context/details are: {details}."
    
    try:
        # Use Gemini model to generate content
        model = genai.GenerativeModel(model_name="models/gemini-pro")  # Adjust the model name as needed
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

# Function to send email
def send_email(subject, body, to_email):
    from_email = st.secrets["FROM_EMAIL"]  # Use Streamlit Secrets for storing email credentials
    password = st.secrets["EMAIL_PASSWORD"]  # Store password securely in Streamlit secrets

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # SMTP server configuration (for Gmail)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

# Streamlit App
def main():
    st.title("Email Assistant")

    # Dropdown to select the reason for the email
    reason = st.selectbox("Select the reason for your email:", 
                          ["Request for Information", "Follow-up", "Job Application", "Thank You", "Inquiry", "Complaint"])

    # User Input Fields
    email_details = st.text_area("Provide the details or context for the email:", height=150)
    subject = st.text_input("Enter the subject of the email:")
    to_email = st.text_input("Enter the recipient's email:")

    if st.button("Generate Email"):
        if email_details and subject and to_email:
            with st.spinner("Generating email..."):
                # Generate email body based on the selected reason and user details
                email_body = generate_email_content(reason, email_details)
                
                if email_body:
                    st.subheader("Generated Email Body:")
                    st.text_area("Email Body:", email_body, height=250)
                    
                    # Option to send the email
                    if st.button("Send Email"):
                        send_email(subject, email_body, to_email)
                
        else:
            st.error("Please fill in all fields.")

if __name__ == "__main__":
    main()
