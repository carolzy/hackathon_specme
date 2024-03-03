import streamlit as st

from templates import display_folder_structure

from function import uml
from function import folder_structure_gen
from function import endpoint_gen
from function import user_feedback

import json
import os
import time

# Constants
LANGUAGES = ["No specific preference", "Python", "JavaScript", "Java",
             "Ruby", "C#", "Go", "PHP", "Swift", "TypeScript", "C++", "other"]

API_FRAMEWORKS = [
    "No specific preference",
    "Express.js with Node.js (Fast, unopinionated, minimalist web framework for Node.js)",
    "Python Flask (A micro web framework written in Python)",
    "Python FastAPI (A modern, fast web framework for building APIs with Python 3.7+)",
    "TypeScript NestJS (A framework for building efficient, reliable and scalable server-side applications)",
    "TypeScript Next.js (A React framework for production - it makes building fullstack React apps and sites a breeze with automatic routing)",
    "Ruby on Rails (A server-side web application framework written in Ruby)",
    "Java Spring Boot (An approach to build stand-alone, production-grade Spring based Applications with ease)",
    "ASP.NET Core (A cross-platform .NET framework for building modern cloud-based web applications on Windows, Mac, or Linux)",
    "Django REST framework (A powerful and flexible toolkit for building Web APIs in Python)",
    "Go Gin (A web framework written in Go (Golang) focusing on performance)",
    "Rust Actix-web (A powerful, pragmatic, and extremely fast web framework for Rust)",
    "other"
]

DATABASES = ["N/A", "MySQL", "MongoDB", "PostgreSQL", "SQLite", "Oracle", "Redis", "Cassandra", "Microsoft SQL Server",
             "Amazon Aurora", "MariaDB", "Amazon DynamoDB", "Couchbase", "Firebase Realtime Database", "Google BigQuery",
                                                            "InfluxDB", "Neo4j", "ArangoDB", "Apache HBase", "IBM Db2", "CouchDB", "No specific preference", "other"]

INTEGRATIONS = ["None needed", "Stripe (Payment Gateway)", "PayPal (Payment Gateway)", "Braintree (Payment Gateway)",  "Google Maps API",
                "Twitter API", "Facebook Graph API", "OAuth 2.0", "JSON Web Tokens (JWT)", "OpenID Connect", "Amazon Web Services (AWS)",
                "Microsoft Azure", "Google Cloud Platform", "Salesforce API", "Twilio API", "Slack API", "Shopify API", "LinkedIn API",
                                                            "Mailchimp API", "Twitch API", "GitHub API", "other"]

# create a language model that summarizes a meeting from transcripts and get the keypoints out of it


def app():

    # SpecMe title
    st.markdown("""
        <h1 style="color: #FF4B4B;">SpecMe</h1>
    """, unsafe_allow_html=True)

    # Button to manually reset state and return to the landing page
    if st.button('Go back to requirements upload'):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state['current_page'] = 'Landing Page'
        st.experimental_rerun()

    ###### page header ###############################################################################################################################
    st.markdown(
        """
        <h5 style='text-align: center;'>From requirements to endpoint</h5>
        """,
        unsafe_allow_html=True
    )

    ###### Body ###############################################################################################################################
    ui_block, uml_block = st.columns([1, 1])

    #### user inputs ########
    with ui_block:
        st.subheader("Endpoint Options")

        # developer's preference
        col1_lang, col2_lang = st.columns([3, 5])
        with col1_lang:
            st.write("")
            st.write('Selected programming language')
        with col2_lang:
            dev_pref_lang = st.selectbox('', LANGUAGES)
            if dev_pref_lang == "other":
                dev_pref_lang = st.text_input("")

        col1_ts, col2_ts = st.columns([3, 5])
        with col1_ts:
            st.write("Selected API framework")
        with col2_ts:
            dev_pref_ts = st.selectbox('', API_FRAMEWORKS)

        col1_db, col2_db = st.columns([3, 5])
        with col1_db:
            st.write("")
            st.write("Selected database")
        with col2_db:
            dev_pref_db = st.selectbox('', DATABASES)
            if dev_pref_db == "other":
                dev_pref_db = st.text_input("")

        col1_integration, col2_integration = st.columns([3, 5])
        with col1_integration:
            st.write("")
            st.write("Extra integrations")
        with col2_integration:
            dev_pref_integration = st.selectbox('', INTEGRATIONS)

            if dev_pref_integration == "more":
                dev_pref_integration = st.text_input("")

        dev_project_req = st.text_area("Tell me about your project", help='please include the description, key features, functionalities of your project',
                                       placeholder='create a language model that summarizes a meeting from transcripts and get the keypoints out of it ... ', height=300)

        text_len = len(dev_project_req.split())
        MAX_LEN = 50
        if text_len > MAX_LEN:
            st.warning(f"Exceeded character limit! maximum word is {MAX_LEN}.")
        else:
            pass

        submit_button = st.button("Submit")
        if submit_button and (text_len < MAX_LEN):
            with st.spinner(" (1/2) analyzing project requirements ..."):
                uml_dict = uml.generate_uml_code(
                    dev_project_req, dev_pref_lang, dev_pref_ts, dev_pref_db, dev_pref_integration)
                st.session_state['uml_dict'] = uml_dict
            with st.spinner(" (2/2) generating UML and Repo structure ..."):
                uml_dir_json = folder_structure_gen.folder_structure_gen(
                    dev_project_req, uml_dict["uml_code"])
                st.session_state['uml_dir_json'] = uml_dir_json

    with uml_block:
        st.subheader('Endpoint UML Diagram')

        # retrieve uml_dict from session state
        uml_dict = st.session_state.get('uml_dict', None)
        if uml_dict is not None:
            st.write(uml_dict["comments"])
            st.image(image=uml_dict["url"], width=750)
            st.markdown(
                f'<a href="{uml_dict["url"]}" target="_blank"><input type="button" value="load uml"></a>',
                unsafe_allow_html=True
            )

        else:
            st.write("(example output) ... waiting for user description ...")
            st.image(image='static/uml_demo.png', width=750)

    # file structure
    st.subheader('Folder Structure')

    uml_dict_session_state = st.session_state.get('uml_dir_json', None)
    if uml_dict_session_state is not None:
        uml_dict_session_state = st.session_state.get('uml_dir_json', None)
        display_folder_structure.display_tree(uml_dict_session_state, ["root"])

        gen_pseudo_buttom = st.button(
            "Approve folder structure and generate pseudo code")
        if gen_pseudo_buttom:
            with st.spinner("Generating pseudo code in repo ..."):
                pseudo_code_json = endpoint_gen.endpoint_generation(
                    dev_project_req, uml_dict['uml_code'], uml_dict_session_state)
                st.session_state['pseudo_code_json'] = pseudo_code_json
                msg_pseu_code = st.success(
                    "pseudo code successfully generated and imported ... ")
                time.sleep(2)
                msg_pseu_code.empty()

        pseudo_code_json = st.session_state.get('pseudo_code_json', None)

        if pseudo_code_json is not None:
            for i in range(len(pseudo_code_json["endpoints"])):
                # Only necessary for displaying directory.
                main_folder = pseudo_code_json["endpoints"][i]['file_path'].split(
                    '/')[0]
                if not uml_dict_session_state['root'].get(main_folder):
                    uml_dict_session_state['root'][main_folder] = dict()
                file_name = pseudo_code_json["endpoints"][i]['file_path'].split(
                    '/')[1]
                code = pseudo_code_json["endpoints"][i]['contents']
                uml_dict_session_state['root'][main_folder][file_name] = code

            st.download_button(
                data=folder_structure_gen.download_repo(
                    pseudo_code_json['endpoints']),
                label="Download Repository",
                file_name="generated_repo.zip",
                mime="application/zip",
                on_click=folder_structure_gen.download_repo,
                args=(pseudo_code_json['endpoints'],)
            )

        else:
            st.write("... start pseudo code generation ...")

    else:
        st.write("(example output) ... waiting for user description ...")
        example_uml = """ 
            {"root": {"transcript_dataset": {"init.py": {}, "data_processing.py": {}, "tests": {"init.py": {}, "test_data_processing.py": {}}}, "language_model": {"init.py": {}, "model.py": {}, "preprocessing.py": {}, "tests": {"init.py": {}, "test_model.py": {}}}, "summarization_module": {"init.py": {}, "summarizer.py": {}, "tests": {"init.py": {}, "test_summarizer.py": {}}}, "key_point_extraction_module": {"init.py": {}, "extractor.py": {}, "tests": {"init.py": {}, "test_extractor.py": {}}}, "config": {"settings.py": {}}, "README.md": {}}}
                    """
        data = json.loads('{"root": {"transcript_dataset": {"init.py": {}, "data_processing.py": {}, "tests": {"init.py": {}, "test_data_processing.py": {}}}, "language_model": {"init.py": {}, "model.py": {}, "preprocessing.py": {}, "tests": {"init.py": {}, "test_model.py": {}}}, "summarization_module": {"init.py": {}, "summarizer.py": {}, "tests": {"init.py": {}, "test_summarizer.py": {}}}, "key_point_extraction_module": {"init.py": {}, "extractor.py": {}, "tests": {"init.py": {}, "test_extractor.py": {}}}, "config": {"settings.py": {}}, "README.md": {}}}')
        display_folder_structure.display_tree(data, ["root"])

    ###### USER FEEDBACK FORM ###############################################################################################################################
    with st.form(key='feedback_form'):
        feedback_str = st.text_input(
            "We're better when we're hearing from you. Share your feedback, ask questions, or discuss opportunities. Let's connect and make great things happen!")
        submit_button = st.form_submit_button('Send')

        if submit_button:
            if feedback_str:
                try:
                    user_feedback.submit_user_feedback(feedback_str)
                    msg_user_feedback_success = st.success(
                        "Message sent successfully!")
                    time.sleep(2)
                    msg_user_feedback_success.empty()
                except Exception as e:
                    msg_user_feedback_error = st.error(
                        f"An error occurred: {str(e)}")
                    time.sleep(2)
                    msg_user_feedback_error.empty()
            else:
                st.error("Please provide some message before submitting!")
