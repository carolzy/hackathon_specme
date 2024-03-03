# app.py
import streamlit as st
from pages import generate_api_options, landing_page, generate_backend, generate_design

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
        "Choose Tech Stack Page": generate_api_options.app,
        "Generate Design": generate_design.app,
        "Generate Backend": generate_backend.app,
    }
    page_function = pages[page]
    page_function()

# Initialize the session state for the current page if it's not already set
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Landing Page"

# Render the current page based on the session state
render_page(st.session_state['current_page'])
