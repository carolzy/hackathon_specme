# app.py
import streamlit as st
from pages import landing_page, generation_page

# Define a function to render the current page
def render_page(page):
    pages = {
        "Landing Page": landing_page.app,
        "Generation Page": generation_page.app,
    }
    page_function = pages[page]
    page_function()

# Initialize the session state for the current page if it's not already set
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Landing Page"

# Render the current page based on the session state
render_page(st.session_state['current_page'])
