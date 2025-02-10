import streamlit as st
import random
import google.generativeai as genai
from fpdf import FPDF
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
genai.api_key = os.getenv('AIzaSyA9UzVlNal1z2PuDQAIsH5Mk0vkHEY1E-U')

# Function to call GenAI API for summarizing content
def generate_summary(text):
    try:
        response = genai.Completion.create(
            model="genai-model",  # Using a hypothetical GenAI model
            prompt=f"Please summarize the following text:\n\n{text}",
            max_tokens=100,  # Adjust max tokens as per your requirement
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"An error occurred while generating the summary: {e}")
        return None

# Function to create a PDF file for the resume
def create_pdf(personal_info, work_experience, education, skills):
    # Creating a PDF document
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Setting title
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Resume", ln=True, align='C')
    
    # Add Personal Info
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {personal_info['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {personal_info['email']}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {personal_info['phone']}", ln=True)
    
    # Add Work Experience
    pdf.ln(10)
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, txt="Work Experience", ln=True)
    pdf.set_font("Arial", size=12)
    for job in work_experience:
        pdf.cell(200, 10, txt=f"{job['role']} at {job['company']}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Details: {job['details']}")
        pdf.ln(5)
    
    # Add Education
    pdf.ln(10)
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, txt="Education", ln=True)
    pdf.set_font("Arial", size=12)
    for edu in education:
        pdf.cell(200, 10, txt=f"{edu['degree']} from {edu['institution']}", ln=True)
        pdf.cell(200, 10, txt=f"Graduation Year: {edu['year']}", ln=True)
        pdf.ln(5)
    
    # Add Skills
    pdf.ln(10)
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, txt="Skills", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=', '.join(skills))
    
    # Save the PDF to a file
    pdf.output("resume.pdf")
    return "resume.pdf"

# Streamlit title and instructions
st.title("Resume Creator Bot")
st.write("Please provide the information below, and I will help you create your resume!")

# Initialize session state to hold collected data
if 'personal_info' not in st.session_state:
    st.session_state.personal_info = {}
if 'work_experience' not in st.session_state:
    st.session_state.work_experience = []
if 'education' not in st.session_state:
    st.session_state.education = []
if 'skills' not in st.session_state:
    st.session_state.skills = []

# Collecting Personal Information
if not st.session_state.personal_info:
    st.header("Personal Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")

    if st.button("Submit Personal Info"):
        st.session_state.personal_info = {'name': name, 'email': email, 'phone': phone}
        st.success("Personal Information Collected!")

# Collecting Work Experience
if st.session_state.personal_info and not st.session_state.work_experience:
    st.header("Work Experience")
    job_role = st.text_input("Job Role")
    company_name = st.text_input("Company Name")
    job_details = st.text_area("Job Details")

    if st.button("Add Job Experience"):
        st.session_state.work_experience.append({'role': job_role, 'company': company_name, 'details': job_details})
        st.success("Work Experience Added!")

# Collecting Education Information
if st.session_state.work_experience and not st.session_state.education:
    st.header("Education")
    degree = st.text_input("Degree")
    institution = st.text_input("Institution")
    grad_year = st.text_input("Graduation Year")

    if st.button("Add Education"):
        st.session_state.education.append({'degree': degree, 'institution': institution, 'year': grad_year})
        st.success("Education Added!")

# Collecting Skills
if st.session_state.education and not st.session_state.skills:
    st.header("Skills")
    skills = st.text_area("Enter Skills (comma-separated)").split(',')

    if st.button("Submit Skills"):
        st.session_state.skills = [skill.strip() for skill in skills if skill.strip()]
        st.success("Skills Added!")

# Final Step: Create and Download the Resume
if st.session_state.skills:
    st.header("Your Resume Summary")
    st.write(f"Name: {st.session_state.personal_info['name']}")
    st.write(f"Email: {st.session_state.personal_info['email']}")
    st.write(f"Phone: {st.session_state.personal_info['phone']}")
    
    st.subheader("Work Experience")
    for job in st.session_state.work_experience:
        st.write(f"{job['role']} at {job['company']}")
        st.write(f"Details: {job['details']}")
    
    st.subheader("Education")
    for edu in st.session_state.education:
        st.write(f"{edu['degree']} from {edu['institution']}, Graduated in {edu['year']}")
    
    st.subheader("Skills")
    st.write(", ".join(st.session_state.skills))


    # Create and download PDF button
    if st.button("Generate Resume"):
        resume_pdf = create_pdf(st.session_state.personal_info, st.session_state.work_experience, st.session_state.education, st.session_state.skills)
        st.success(f"Your resume has been created! Download it below.")
        with open(resume_pdf, "rb") as f:
            st.download_button("Download Resume", f, file_name="resume.pdf", mime="application/pdf")
