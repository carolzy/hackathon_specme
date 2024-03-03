# pages/landing_page.py
import streamlit as st

def app():
    # Logo and redirection JavaScript
    # SpecMe title and redirection JavaScript
    st.markdown("""
        <a href="javascript:void(0);" onclick="resetState();" style="text-decoration: none;">
            <h1 style="color: #FF4B4B; cursor: pointer;">SpecMe</h1>
        </a>
        <script>
            function resetState(){
                // Reset all session states
                const keys = [...Object.keys(window.parent.window.streamlitShareMetadata.sessionState)];
                keys.forEach(key => {
                    window.parent.window.streamlit.sessionState[key] = undefined;
                });
                window.parent.window.streamlit.sessionState['current_page'] = 'Landing Page'; // Set the page to the landing page
                window.parent.window.streamlit.forceRerun();
            }
        </script>
    """, unsafe_allow_html=True)
    st.title('Welcome to YOBO')
    st.subheader('Your One-Stop Solution for UML Design and Repo Generation')
    st.write('YOBO is an innovative platform that assists developers from the initial UML design to the final repository generation.')

    # Create a file uploader widget
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'])

    if st.button('Go to Generation Page'):
        if uploaded_file is not None:
            # Check the file's type
            file_type = uploaded_file.type
            
            # Process the file based on its type
            if file_type == "application/pdf":
                st.write("You have uploaded a PDF file.")
                st.session_state['current_page'] = 'Generation Page'  # Update the session state
                st.experimental_rerun()
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                st.write("You have uploaded a Microsoft Word file.")
                st.session_state['current_page'] = 'Generation Page'  # Update the session state
                st.experimental_rerun()
            elif file_type == "text/plain":
                st.write("You have uploaded a text file.")
                st.session_state['current_page'] = 'Generation Page'  # Update the session state            
                st.experimental_rerun()
            else:
                st.error("Unsupported file format!")
        else:
            st.error("Please upload a file to proceed.")
