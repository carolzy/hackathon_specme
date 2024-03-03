# landing_page.py
import time
import streamlit as st
import pdfplumber
from docx import Document

from function.gpt import GPTInstance  # Adjust import path as necessary

# Initialize the GPT-4 instance
gpt_instance = GPTInstance()

def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return " ".join(pages)

def read_docx(file):
    doc = Document(file)
    return " ".join(paragraph.text for paragraph in doc.paragraphs)

def app():
    if 'validated' not in st.session_state:
        st.session_state.validated = False

    if st.session_state.validated:
        # If already validated, skip to avoid displaying this page again.
        return

    st.subheader('Go from requirements document to functioning endpoint instantly!')

    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'], key="file_uploader")

    text_input = st.text_area("Or type your requirements here", key="text_input")
    
    if st.button('Validate and Proceed', key="proceed_button"):
        if uploaded_file is not None or text_input:
            with st.spinner('Validating document...'):
                # Determine the file type and extract text
                text = None
                if text_input:
                    text = text_input
                elif uploaded_file.type == "application/pdf":
                    text = read_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = read_docx(uploaded_file)
                elif uploaded_file.type == "text/plain":
                    text = str(uploaded_file.read(), 'utf-8')
                else:
                    st.error("Unsupported file format!")
                    return

                if text:  # Proceed with validation only if text was extracted
                    # Use the GPTInstance to check if the document lists product requirements
                    gpt_response = gpt_instance(input=f'Here is the content from a document:\n{text}\n\nReturn YES if the content describes requirements for a product and NO if it does not. Respond with 5 words and nothing else.', max_tokens=5)
                    
            # Validate the response
            if "YES" in gpt_response.content.upper():
                st.session_state.validated = True
                st.session_state['current_page'] = 'Choose Tech Stack Page'
                st.session_state['requirements_text'] = text
                st.success('Done!')
            else:
                st.error("The uploaded document does not seem to be a valid requirements document. Please upload a document listing the product requirements.")
        else:
            st.error("Please upload a file to proceed.")
    
    if st.session_state.validated:
        st.experimental_rerun()
