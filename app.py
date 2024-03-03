# app.py
import streamlit as st
from pages import landing_page, generation_page

import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)

# Define a function to render the current page
###### page config ###############################################################################################################################
st.set_page_config(
    page_title="specme",
    page_icon="static/yobo_icon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            body {margin-top: -20px;} /* Adjust this value as needed */
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


###### page header ###############################################################################################################################
st.markdown(
    """
    <h1 style='text-align: center;'>SpecMe</h1>
    <h5 style='text-align: center;'>From PRD to Repo generation in seconds.</h5>
    """,
    unsafe_allow_html=True
)

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
