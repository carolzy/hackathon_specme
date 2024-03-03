# pages/2_Choose_Tech_Stack.py
import streamlit as st
from function import uml
from function import folder_structure_gen

from function.gpt import GPTInstance  # Ensure this import is correct based on your project structure

# Initialize GPT-4 instance
gpt_instance = GPTInstance()

LANGUAGES = ["Python", "JavaScript", "Java",
             "Ruby", "C#", "Go", "PHP", "Swift", "TypeScript", "C++", "other"]

API_FRAMEWORKS = [
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

def button_clicked():
    st.session_state['current_page'] = 'Generate Design'

def app():
     # Clearing the spinner session state if it was set on a previous page
    st.subheader("Choose Tech Stack")

    # Initialize session state for selections if not already set
    if 'recommended_language' not in st.session_state:
        st.session_state['recommended_language'] = None
    if 'recommended_framework' not in st.session_state:
        st.session_state['recommended_framework'] = None
    if 'recommended_databases' not in st.session_state:
        st.session_state['recommended_databases'] = []
    if 'recommended_integrations' not in st.session_state:
        st.session_state['recommended_integrations'] = []

    if not st.session_state['recommended_language'] and not st.session_state['recommended_framework'] and not len(st.session_state['recommended_databases'] ) and not len(st.session_state['recommended_integrations'] ):
        # with ui_block:
            text = st.session_state.get('requirements_text', '')
            # Programming language selection
            st.write("Selected programming language:")
            # Display loading bar if recommendation is pending
            if st.session_state['recommended_language'] is None:
                with st.spinner('Generating recommended programming language...'):
                    recommended_language = gpt_instance(input=f'Given these requirements:\n{text}\n Recommend a programming language to use based on simplicity of implementation and integrations out of the following languages: [{"".join(LANGUAGES)}]? Respond ONLY with ONE programming language and nothing else.', max_tokens=5).content
                    # Extract and update language choice
                    st.session_state['recommended_language'] = recommended_language
                # Allow user to select or change language
                options = LANGUAGES + [st.session_state['recommended_language']] if st.session_state['recommended_language'] not in LANGUAGES else LANGUAGES
                st.session_state['recommended_language'] = st.selectbox('', options, index=options.index(st.session_state['recommended_language']))

            # API framework selection
            st.write("Selected API framework:")
            if st.session_state['recommended_framework'] is None:
                with st.spinner('Generating recommended API framework...'):
                    # Assume requirements text is stored in session state
                    recommended_framework = gpt_instance(input=f'Given these requirements:\n{text}\n Given also that we are using this language:\n{recommended_language}\n Recommend an API framework to use based on simplicity of implementation, compatibility with requirements, and available integrations out of the following API frameworks: [{"".join(API_FRAMEWORKS)}]? Respond ONLY with ONE API framework and nothing else.', max_tokens=10).content
                    st.session_state['recommended_framework'] = recommended_framework
                options_framework = list(set(API_FRAMEWORKS + [st.session_state['recommended_framework']]))
                st.session_state['recommended_framework'] = st.selectbox('', options_framework, index=options_framework.index(st.session_state['recommended_framework']))

            # Database selection
            st.write("Selected database(s):")
            # For the database selection with dynamic addition based on GPT recommendations
            max_db_recommendations = 3  # Set the maximum number of database recommendations
            # Loop for multiple database recommendations
            for i in range(max_db_recommendations):
                # Check if we need to generate a new recommendation
                if i >= len(st.session_state['recommended_databases']):
                    with st.spinner(f'Generating recommendation for database #{i+1}...'):
                         # Construct the prompt with previously selected databases
                         previous_dbs = ', '.join(st.session_state['recommended_databases'])
                         recommended_db = gpt_instance(input=f'Given these requirements:\n{text}\n Given also that we are using this language {recommended_language} with this API framework {recommended_framework} and given that we are already using these databases [{previous_dbs}], recommend a database to use based on simplicity of use, compatibility with requirements, language, and API framework, ease of use, popularity in developer community, efficiency, and scalability out of the following databases: [{"".join(DATABASES)}]? If the requirements do not require a database or we are already using sufficiently many databases, choose the "None needed" option. Respond ONLY with ONE option and NOTHING else.', max_tokens=10).content.strip()
                        # Update the session state only if recommended database is not 'None needed'
                         if "none needed" in recommended_db.lower() and i > 0:
                            break
                         else:
                            st.session_state['recommended_databases'].append(recommended_db)

                # Always show the dropdown to allow user selection or change; ensure the dropdown appears even if recommendation is 'None needed'
                current_option = st.session_state['recommended_databases'][i] if i < len(st.session_state['recommended_databases']) else "None needed"
                selected_db = st.selectbox(f'Selected database #{i+1}:', DATABASES + [current_option], index=(DATABASES + [current_option]).index(current_option) if current_option in DATABASES else len(DATABASES))
                # Update the session state based on user selection
                if i < len(st.session_state['recommended_databases']):
                    st.session_state['recommended_databases'][i] = selected_db
                elif selected_db != "None needed":
                     st.session_state['recommended_databases'].append(selected_db)


            st.write("Selected additional integration(s):")
            max_integ_recommendations = 3  # Set the maximum number of database recommendations
            # Loop for multiple database recommendations
            for i in range(max_integ_recommendations):
                # Check if we need to generate a new recommendation
                if i >= len(st.session_state['recommended_integrations']):
                     with st.spinner(f'Generating recommendation for integration #{i+1}...'):
                        # Construct the prompt with previously selected databases
                         previous_integs = ', '.join(st.session_state['recommended_integrations'])
                         recommended_integ = gpt_instance(input=f'Given these requirements:\n{text}\n Given also that we are using this language {recommended_language} with this API framework {recommended_framework} and given that we are already using these integrations [{previous_integs}], recommend an integration that is necessary for satisfying the requirements of the app we are building fro the following integratiions: [{"".join(INTEGRATIONS)}]? If the requirements do not require an integration or we are already using sufficiently many integrations, choose the "None needed" option. Respond ONLY with ONE option and NOTHING else.', max_tokens=10).content.strip()
                         # Update the session state only if recommended database is not 'None needed'
                         if "none needed" in recommended_integ.lower() and i > 0:
                            break
                         else:
                            st.session_state['recommended_integrations'].append(recommended_integ)

                # Always show the dropdown to allow user selection or change; ensure the dropdown appears even if recommendation is 'None needed'
                current_option = st.session_state['recommended_integrations'][i] if i < len(st.session_state['recommended_integrations']) else "None needed"
                selected_integ = st.selectbox(f'Selected integration #{i+1}:', INTEGRATIONS + [current_option], index=( INTEGRATIONS + [current_option]).index(current_option) if current_option in INTEGRATIONS else len(INTEGRATIONS))
                # Update the session state based on user selection
                if i < len(st.session_state['recommended_integrations']):
                    st.session_state['recommended_integrations'][i] = selected_integ
                elif selected_db != "None recommended_integrations":
                    st.session_state['recommended_integrations'].append(selected_integ)
            
     # Button to proceed to the next step, should be enabled only after all selections are made
    st.button("Step 3: Generate UML", on_click=button_clicked)