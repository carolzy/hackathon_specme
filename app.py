# app.py
import streamlit as st
from pages import landing_page, generation_page, choose_tech_stack

import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)

# Define a function to render the current page
###### page config ###############################################################################################################################
st.set_page_config(
        page_title="yobo",
        page_icon="static/yobo_icon.png",
        layout="wide",
        initial_sidebar_state="collapsed"
)

def render_page(page):
    pages = {
        "Landing Page": landing_page.app,
        "Generation Page": generation_page.app,
        "Choose Tech Stack Page": choose_tech_stack.app,
    }
    page_function = pages[page]
    page_function()

# Initialize the session state for the current page if it's not already set
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Landing Page"

# Render the current page based on the session state
render_page(st.session_state['current_page'])
