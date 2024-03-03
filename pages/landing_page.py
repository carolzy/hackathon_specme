# pages/landing_page.py
import streamlit as st
import pdfplumber
from docx import Document
from io import BytesIO

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

    st.subheader('Go from requirements document to functioning endpoint instantly!')

    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'], key="file_uploader")

    # Define a variable to track document validation status
    validated = False

    # Button to proceed; the logic below will determine if it should lead to an action
    proceed = st.button('Validate and Proceed', key="proceed_button")

    # Check if the file is uploaded and the button is pressed
    if proceed:
        if uploaded_file is not None:
            with st.spinner('Validating document...'):
                # Determine the file type and extract text
                if uploaded_file.type == "application/pdf":
                    text = read_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = read_docx(uploaded_file)
                elif uploaded_file.type == "text/plain":
                    text = str(uploaded_file.read(), 'utf-8')  # Assuming UTF-8 encoding
                else:
                    st.error("Unsupported file format!")
                    return

                # Use the GPTInstance to check if the document lists product requirements
                gpt_response = gpt_instance(input=f'Here is the content from a document:\n{text}\n\n Return YES if the content describes requirements for a product and NO if it does not. Respond with 5 words and nothing else.', max_tokens=5)
                
                # Validate the response
                print(gpt_response)
                print(gpt_response.content)
                if "YES" in gpt_response.content.upper():
                    validated = True
                else:
                    validated = False
                    st.error("The uploaded document does not seem to be a valid requirements document. Please upload a document listing the product requirements.")

            # If document is validated, proceed to the next page
            if validated:
                st.session_state['current_page'] = 'Choose Tech Stack Page'
                st.session_state['requirements_text'] = text
                st.experimental_rerun()
        else:
            st.error("Please upload a file to proceed.")
