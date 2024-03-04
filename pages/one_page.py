import streamlit as st
import traceback
from templates import display_folder_structure

from function import uml
from function import folder_structure_gen
from function import endpoint_gen
from function import user_feedback
from function import class_diagram

import json
import zipfile
import requests
import os
import time
import pdfplumber
from docx import Document

from function.gpt import GPTInstance  # Adjust import path as necessary

# Initialize the GPT-4 instance
gpt_instance = GPTInstance()

VERCEL_TOKEN = 'OWCHQTXMOhuuvM2qBYPyNaSB'
PROJECT_DIR = '/Users/spandana/Desktop/generated_repo.zip'
ZIP_FILE_NAME = 'project.zip'

LANGUAGES = ["Python", "JavaScript", "Java",
             "Ruby", "C#", "Go", "PHP", "Swift", "TypeScript", "C++", "other", ""]

API_FRAMEWORKS = [
    "",
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

DATABASES = ["None needed", "MySQL", "Pinecone Vector DB", "MongoDB", "PostgreSQL", "SQLite", "Oracle", "Redis", "Cassandra", "Microsoft SQL Server",
             "Amazon Aurora", "MariaDB", "Amazon DynamoDB", "Couchbase", "Firebase Realtime Database", "Google BigQuery",
                                                            "InfluxDB", "Neo4j", "ArangoDB", "Apache HBase", "IBM Db2", "CouchDB", "No specific preference", "other"]

INTEGRATIONS = ["None needed", "OpenAI LLM Generations Endpoints","Serper API for programmatically searching the web ",  "Stripe (Payment Gateway)", "PayPal (Payment Gateway)", "Braintree (Payment Gateway)",  "Google Maps API",
                "Twitter API", "Facebook Graph API", "OAuth 2.0", "JSON Web Tokens (JWT)", "OpenID Connect", "Amazon Web Services (AWS)",
                "Microsoft Azure", "Google Cloud Platform", "Salesforce API", "Twilio API", "Slack API", "Shopify API", "LinkedIn API",
                                                            "Mailchimp API", "Twitch API", "GitHub API", "other"]


def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return " ".join(pages)

def read_docx(file):
    doc = Document(file)
    return " ".join(paragraph.text for paragraph in doc.paragraphs)

# Zip your project directory
def zip_project(directory, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(directory, '..')))

# Deploy zip file to Vercel
def deploy_to_vercel(zip_file, token, team_id=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/zip',
    }
    files = {'file': open(zip_file, 'rb')}
    params = {}
    if team_id:
        params['teamId'] = team_id

    response = requests.post('https://api.vercel.com/v12/now/deployments', headers=headers, files=files, params=params)
    return response.json()

def app():
    ###### page header ###############################################################################################################################
    st.markdown(
        """
        <h1 style='text-align: center;'>SpecMe</h1>
        <h5 style='text-align: center;'>From PRD to Backend Code</h5>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state for selections if not already set
    if 'recommended_language' not in st.session_state:
        st.session_state['recommended_language'] = None
    if 'recommended_framework' not in st.session_state:
        st.session_state['recommended_framework'] = None
    if 'recommended_database' not in st.session_state:
        st.session_state['recommended_database'] = None
    if 'recommended_databases' not in st.session_state:
        st.session_state['recommended_databases'] = []
    if 'recommended_integrations' not in st.session_state:
        st.session_state['recommended_integrations'] = []
    if 'recommended_integration' not in st.session_state:
        st.session_state['recommended_integration'] = None

    ###### Body ###############################################################################################################################

    # PRD Block
    st.subheader('Go from requirements document to functioning endpoint instantly!')
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'], key="file_uploader")
    #text_input = st.text_area("Or type your requirements here", key="text_input")

    if st.button('Validate and Proceed', key="proceed_button"):
        if uploaded_file is not None:
            with st.spinner('Validating document...'):
                # Determine the file type and extract text
                if uploaded_file.type == "application/pdf":
                    text = read_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = read_docx(uploaded_file)
                elif uploaded_file.type == "text/plain":
                    text = str(uploaded_file.read(), 'utf-8')
                else:
                    st.error("Unsupported file format!")

                if text:  # Proceed with validation only if text was extracted
                    # Use the GPTInstance to check if the document lists product requirements
                    gpt_response = gpt_instance(input=
                                                f'Here is the content from a document:\n{text}\n\nReturn YES if the content describes requirements for a product and NO if it does not. Respond with 5 words and nothing else.', max_tokens=5)
                    
            # Validate the response
            if "YES" in gpt_response.content.upper():
                st.session_state.validated = True
                st.session_state['requirements_text'] = text

                if st.session_state['recommended_language'] is None:
                    with st.spinner('Generating recommended programming language...'):
                        recommended_language = gpt_instance(input=f'Given these requirements:\n{text}\n Recommend a programming language to use based on simplicity of implementation and integrations out of the following languages: [{"".join(LANGUAGES)}]? Respond ONLY with ONE programming language and nothing else.', max_tokens=5).content
                        # Extract and update language choice
                        st.session_state['recommended_language'] = recommended_language
                if st.session_state['recommended_framework'] is None:
                    with st.spinner('Generating recommended API framework...'):
                        # Assume requirements text is stored in session state
                        recommended_framework = gpt_instance(input=f'Given these requirements:\n{text}\n Given also that we are using this language:\n{recommended_language}\n Recommend an API framework to use based on simplicity of implementation, compatibility with requirements, and available integrations out of the following API frameworks: [{"".join(API_FRAMEWORKS)}]? Respond ONLY with ONE API framework and nothing else.', max_tokens=10).content
                        st.session_state['recommended_framework'] = recommended_framework
                if st.session_state['recommended_database'] is None:
                    # For the database selection with dynamic addition based on GPT recommendations
                    with st.spinner(f'Generating recommendation for database...'):
                        max_db_recommendations = 3  # Set the maximum number of database recommendations
                        # Loop for multiple database recommendations
                        for i in range(max_db_recommendations):
                            # Check if we need to generate a new recommendation
                            if i >= len(st.session_state['recommended_databases']):
                                # Construct the prompt with previously selected databases
                                previous_dbs = ', '.join(st.session_state['recommended_databases'])
                                recommended_db = gpt_instance(input=f'Given these requirements:\n{text}\n Given also that we are using this language {recommended_language} with this API framework {recommended_framework} and given that we are already using these databases [{previous_dbs}], recommend a database to use based on simplicity of use, compatibility with requirements, language, and API framework, ease of use, popularity in developer community, efficiency, and scalability out of the following databases: [{"".join(DATABASES)}]? If the requirements do not require a database or we are already using sufficiently many databases, choose the "None needed" option. Respond ONLY with ONE option and NOTHING else.', max_tokens=10).content.strip()
                                # Update the session state only if recommended database is not 'None needed'
                                if "none needed" in recommended_db.lower() and i > 0:
                                    break
                                else:
                                    st.session_state['recommended_databases'].append(recommended_db)
                if st.session_state['recommended_integration'] is None:
                    with st.spinner(f'Generating recommendation for integration...'):
                        max_integ_recommendations = 3  # Set the maximum number of database recommendations
                        # Loop for multiple database recommendations
                        for i in range(max_integ_recommendations):
                                # Check if we need to generate a new recommendation
                                if i >= len(st.session_state['recommended_integrations']):
                                    # Construct the prompt with previously selected databases
                                    previous_integs = ', '.join(st.session_state['recommended_integrations'])
                                    recommended_integ = gpt_instance(input=f'Given these requirements:\n{text}\n Given also that we are using this language {recommended_language} with this API framework {recommended_framework} and given that we are already using these integrations [{previous_integs}], recommend an integration that is necessary for satisfying the requirements of the app we are building fro the following integratiions: [{"".join(INTEGRATIONS)}]? If the requirements do not require an integration or we are already using sufficiently many integrations, choose the "None needed" option. Respond ONLY with ONE option and NOTHING else.', max_tokens=10).content.strip()
                                    # Update the session state only if recommended database is not 'None needed'
                                    if "none needed" in recommended_integ.lower() and i > 0:
                                        break
                                    else:
                                        st.session_state['recommended_integrations'].append(recommended_integ)
                        # st.success('Done!')
            else:
                st.error("The uploaded document does not seem to be a valid requirements document. Please upload a document listing the product requirements.")
        else:
            st.error("Please upload a file to proceed.")

    ui_block = st.container()
    uml_block, class_block = st.columns([1, 1])
    folder_block = st.container()

    #### user inputs ########
    with ui_block:
        st.subheader("Choose Tech Stack")
        text = st.session_state.get('requirements_text', '')

        # developer's preference
        if st.session_state['recommended_language'] is not None:
            default_value = st.session_state['recommended_language']
        else:
            default_value = ''
        
        #print(default_value)
        dev_pref_lang = st.selectbox('Preferred programming language?', LANGUAGES, index=LANGUAGES.index(default_value))

        if st.session_state['recommended_framework'] is not None:
            default_value = st.session_state['recommended_framework']
        else:
            default_value = ""
        
        #print(default_value)
        for i in API_FRAMEWORKS:
            if default_value in i:
                default_value = i
                break
        dev_pref_ts = st.selectbox('Preferred API framework?', API_FRAMEWORKS, index=API_FRAMEWORKS.index(default_value))

        if len(st.session_state['recommended_databases']) > 0 :
            default_value = st.session_state['recommended_databases'][0]
        else:
            default_value = "None needed"
        
        #print(default_value)
        dev_pref_db = st.selectbox('Preferred database?', DATABASES, index=DATABASES.index(default_value))

        if len(st.session_state['recommended_integrations']) > 0:
            default_value = st.session_state['recommended_integrations'][0]
        else:
            default_value = 'None needed'
        
        #print(default_value)
        dev_pref_integration = st.selectbox('Preferred third-party integrations?', INTEGRATIONS, index=INTEGRATIONS.index(default_value))
        
        uml_dict = st.session_state.get('uml_dict', None)
        class_dict = st.session_state.get('class_dict', None)
        submit_button = st.button("Generate UML Diagram and Repo Structure")
        # st.image(image='static/padding.png', width=750)
        # st.image(image='static/padding.png', width=750)
        if submit_button:
            with st.spinner(" (1/3) Generating UML diagram ..."):
                uml_dict = uml.generate_uml_code(text, dev_pref_lang, dev_pref_ts, dev_pref_db, dev_pref_integration)
                st.session_state['uml_dict'] = uml_dict 
            with st.spinner(" (2/3) Generating Class diagram ..."):
                class_dict = class_diagram.generate_class_diagram_code(text, dev_pref_lang, dev_pref_ts, dev_pref_db, dev_pref_integration)
                st.session_state['class_dict'] = class_dict 
            with st.spinner(" (3/3) generating Repo structure ..."):
                uml_dir_json = folder_structure_gen.folder_structure_gen(text, dev_pref_lang, uml_dict["uml_code"])
                st.session_state['uml_dir_json'] = uml_dir_json


    with uml_block:
        st.subheader('UML Diagram')

        uml_dict = st.session_state.get('uml_dict', None) # retrieve uml_dict from session state
        if uml_dict is not None:
            st.write(uml_dict["comments"])
            st.image(image=uml_dict["url"]
                    , width = 750)
            # st.markdown(
            #     f'<a href="{uml_dict["url"]}" target="_blank"><input type="button" value="load uml"></a>',
            #     unsafe_allow_html=True
            # )

        else:
            st.write("(example output) ... waiting for user description ...")
            st.image(image='static/uml_demo.png', width = 750)

    
    with class_block:
        st.subheader('Class Diagram')

        class_dict = st.session_state.get('class_dict', None) # retrieve uml_dict from session state
        if class_dict is not None:
            st.write(class_dict["comments"])
            st.image(image=class_dict["url"]
                    , width = 750)
            # st.markdown(
            #     f'<a href="{uml_dict["url"]}" target="_blank"><input type="button" value="load uml"></a>',
            #     unsafe_allow_html=True
            # )

        else:
            st.write("(example output) ... waiting for user description ...")
            st.image(image='static/class_demo.png', width = 750)
        
    with folder_block:
        # file structure 
        st.subheader('Folder Structure')
        try: 
            uml_dict_session_state = st.session_state.get('uml_dir_json', None)
            if uml_dict_session_state is not None:
                uml_dict_session_state = st.session_state.get('uml_dir_json', None)
                if (isinstance(uml_dict_session_state, str)):
                    uml_dict_session_state = json.loads(uml_dict_session_state)
                display_folder_structure.display_tree(uml_dict_session_state, ["root"])
                gen_pseudo_buttom = st.button("Approve folder structure and generate pseudo code")
                
                if gen_pseudo_buttom:
                    with st.spinner("Generating pseudo code in repo ..."):
                        pseudo_code_json = endpoint_gen.endpoint_generation(st.session_state['requirements_text'], uml_dict['uml_code'], '', dev_pref_lang, uml_dict_session_state)
                        st.session_state['pseudo_code_json'] = pseudo_code_json 
                        msg_pseu_code = st.success("pseudo code successfully generated and imported ... ")
                        time.sleep(2)
                        msg_pseu_code.empty()
                
                pseudo_code_json = st.session_state.get('pseudo_code_json', None)
                print(pseudo_code_json)
                if pseudo_code_json is not None:
                    print('psuedo code not none', pseudo_code_json)
                    for i in range(len(json.loads(pseudo_code_json["endpoints"]))):
                        # Only necessary for displaying directory.
                        main_folder = pseudo_code_json["endpoints"][i]['file_path'].split('/')[0]
                        if not uml_dict_session_state['root'].get(main_folder):
                            uml_dict_session_state['root'][main_folder] = dict()
                        file_name = pseudo_code_json["endpoints"][i]['file_path'].split('/')[1]
                        code = pseudo_code_json["endpoints"][i]['contents']
                        uml_dict_session_state['root'][main_folder][file_name] = code
                    print('render download button')
                    st.download_button(
                        data=folder_structure_gen.download_repo(pseudo_code_json['endpoints']),
                        label="Download Repository",
                        file_name="generated_repo.zip",
                        mime="application/zip",
                        on_click=folder_structure_gen.download_repo,
                        args=(pseudo_code_json['endpoints'],)
                    )

                    deploy_code = st.button('Deploy code')
                    if deploy_code:
                        zip_project(PROJECT_DIR, ZIP_FILE_NAME)
                        deployment_response = deploy_to_vercel(ZIP_FILE_NAME, VERCEL_TOKEN, '')
                        
                        if deployment_response.get('error'):
                            st.write(f"Error deploying to Vercel: {deployment_response.get('error')}")
                        else:
                            deployment_url = deployment_response.get('url')
                            st.write(f"Deployment successful! Your project is live at: https://{deployment_url}")

                    
                else:
                    st.write("... start pseudo code generation ...")

            else:
                st.write("(example output) ... waiting for user description ...")
                example_uml = """ 
                    {"root": {"transcript_dataset": {"init.py": {}, "data_processing.py": {}, "tests": {"init.py": {}, "test_data_processing.py": {}}}, "language_model": {"init.py": {}, "model.py": {}, "preprocessing.py": {}, "tests": {"init.py": {}, "test_model.py": {}}}, "summarization_module": {"init.py": {}, "summarizer.py": {}, "tests": {"init.py": {}, "test_summarizer.py": {}}}, "key_point_extraction_module": {"init.py": {}, "extractor.py": {}, "tests": {"init.py": {}, "test_extractor.py": {}}}, "config": {"settings.py": {}}, "README.md": {}}}
                            """
                data = json.loads('{"root": {"transcript_dataset": {"init.py": {}, "data_processing.py": {}, "tests": {"init.py": {}, "test_data_processing.py": {}}}, "language_model": {"init.py": {}, "model.py": {}, "preprocessing.py": {}, "tests": {"init.py": {}, "test_model.py": {}}}, "summarization_module": {"init.py": {}, "summarizer.py": {}, "tests": {"init.py": {}, "test_summarizer.py": {}}}, "key_point_extraction_module": {"init.py": {}, "extractor.py": {}, "tests": {"init.py": {}, "test_extractor.py": {}}}, "config": {"settings.py": {}}, "README.md": {}}}')
                #display_folder_structure.display_tree(data, ["root"])
        
        except Exception as e:
                print(e)
                print(traceback.format_exc())
                example_uml = """ 
                    {"root": {"transcript_dataset": {"init.py": {}, "data_processing.py": {}, "tests": {"init.py": {}, "test_data_processing.py": {}}}, "language_model": {"init.py": {}, "model.py": {}, "preprocessing.py": {}, "tests": {"init.py": {}, "test_model.py": {}}}, "summarization_module": {"init.py": {}, "summarizer.py": {}, "tests": {"init.py": {}, "test_summarizer.py": {}}}, "key_point_extraction_module": {"init.py": {}, "extractor.py": {}, "tests": {"init.py": {}, "test_extractor.py": {}}}, "config": {"settings.py": {}}, "README.md": {}}}
                            """
                data = json.loads('{"root": {"transcript_dataset": {"init.py": {}, "data_processing.py": {}, "tests": {"init.py": {}, "test_data_processing.py": {}}}, "language_model": {"init.py": {}, "model.py": {}, "preprocessing.py": {}, "tests": {"init.py": {}, "test_model.py": {}}}, "summarization_module": {"init.py": {}, "summarizer.py": {}, "tests": {"init.py": {}, "test_summarizer.py": {}}}, "key_point_extraction_module": {"init.py": {}, "extractor.py": {}, "tests": {"init.py": {}, "test_extractor.py": {}}}, "config": {"settings.py": {}}, "README.md": {}}}')
                #display_folder_structure.display_tree(data, ["root"])
