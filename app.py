import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
      model = genai.GenerativeModel("gemini-1.5-flash")
      response= model.generate_content(input)
      return response.text

def input_pdf_text(uploaded_file):
      if uploaded_file is not None:
            pdf_reader = pdf.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                  text += page.extract_text()
            return text
      else:
            raise FileNotFoundError("No file uploaded")
      
input_prompt = """
You are an extremely experienced and skilled Application Tracking System (ATS) with in-depth knowledge of how modern hiring systems scan, match, and evaluate resumes. 
You are also trained in technical recruiting across domains including:
- Software Engineering
- Full Stack Development
- DevOps
- Data Science
- Big Data Engineering
- Data Analytics
- Cloud and Infrastructure

You will be given:
1. A resume (in image or text form) of a candidate.
2. A job description that outlines required qualifications, responsibilities, and keywords.

Your task is to:
- **Match the resume against the job description using ATS-style parsing**
- **Calculate a JD Match Score** (as a percentage) representing how closely the resume aligns with the job.
- **List Missing Keywords**: Any relevant keywords or skills from the JD that are not found in the resume.
- **Provide a Professional Summary** (as a recruiter or career coach would), commenting on the candidate’s suitability for the role, strengths, and improvement areas.

Make sure the evaluation includes both:
- **Hard Skills Match** (e.g., Python, SQL, AWS, CI/CD)
- **Soft Skills or Responsibilities** (e.g., "collaborate with cross-functional teams", "lead architecture discussions")

Be honest, unbiased, and helpful.

---

📄 **INPUT FORMAT**  
Resume: {text}  
Job Description: {jd}

---

📦 OUTPUT FORMAT:
Return in JSON (in one line):
{{
  "JD Match": "XX%",  
  "MissingKeywords": ["keyword1", "keyword2"],  
  "ProfileSummary": "..."  
}}

DO NOT return markdown, formatting, or extra text. Only the JSON string as specified above.

"""

# Streamlit app
st.set_page_config(
    page_title="ATS Resume Evaluator",    
    page_icon="favicon.png",                         
    layout="centered",                   
    initial_sidebar_state="auto"
)


st.title("ATS Resume Evaluator")
st.text("Improve your resume ATS")
jd=st.text_area("Paste the Job Description here")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"], help="Upload your resume in PDF format for evaluation")
submit = st.button("Evaluate Resume")

if submit:
      if uploaded_file is not None:
            resume_text = input_pdf_text(uploaded_file)
            final_prompt = input_prompt.format(text=resume_text, jd=jd)
            response = get_gemini_response(final_prompt)
            st.subheader(response)
      else:
            st.error("Please upload a valid PDF resume file.")
