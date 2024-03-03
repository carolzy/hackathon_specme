# app.py
import streamlit as st
from pages import landing_page, choose_tech_stack, generate_backend, generate_design, generation_page

# import sys
# print("Python executable:", sys.executable)
# print("Python version:", sys.version)

# Define a function to render the current page
###### page config ###############################################################################################################################
st.set_page_config(
        page_title="specme",
        page_icon="static/yobo_icon.png",
        layout="wide",
        initial_sidebar_state="collapsed"
)

def render_page(page):
    pages = {
        "Landing Page": landing_page.app,
        "Generation Page": generation_page.app,
        "Choose Tech Stack Page": choose_tech_stack.app,
        "Generate Design": generate_design.app,
        "Generate Backend": generate_backend.app,
    }
    page_function = pages[page]
    page_function()

# Initialize the session state for the current page if it's not already set
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Generate Design"

# Render the current page based on the session state
render_page(st.session_state['current_page'])
