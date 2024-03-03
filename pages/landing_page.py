# pages/landing_page.py
import streamlit as st

def app():
    st.title('Welcome to YOBO')
    st.subheader('Your One-Stop Solution for UML Design and Repo Generation')
    st.write('YOBO is an innovative platform that assists developers from the initial UML design to the final repository generation.')

    # Button to navigate to the Generation Page
    if st.button('Go to Generation Page'):
        st.session_state['current_page'] = 'Generation Page'  # Update the session state