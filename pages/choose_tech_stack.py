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

INTEGRATIONS = ["None needed", "OpenAI LLM Generations", "OpenAI Dalle-2", "Auth0 for authentication", "Serper API for programmatically searching the web ",  "Stripe (Payment Gateway)", "PayPal (Payment Gateway)", "Braintree (Payment Gateway)",  "Google Maps API",
                "Twitter API", "Facebook Graph API", "OAuth 2.0", "JSON Web Tokens (JWT)", "OpenID Connect", "Amazon Web Services (AWS)",
                "Microsoft Azure", "Google Cloud Platform", "Salesforce API", "Twilio API", "Slack API", "Shopify API", "LinkedIn API",
                                                            "Mailchimp API", "Twitch API", "GitHub API", "other"]


def app():
    st.subheader("Choose Tech Stack")
    ui_block, uml_block = st.columns([0.8, 0.2])

    # Initialize session state for selections if not already set
    if 'recommended_language' not in st.session_state:
        st.session_state['recommended_language'] = None
    if 'recommended_framework' not in st.session_state:
        st.session_state['recommended_framework'] = None
    if 'recommended_database' not in st.session_state:
        st.session_state['recommended_database'] = None
    if 'recommended_integrations' not in st.session_state:
        st.session_state['recommended_integrations'] = None

    with ui_block:
        # Programming language selection
        col1_lang, col2_lang = st.columns([3, 5])
        with col1_lang:
            st.write("Selected programming language:")
        with col2_lang:
            # Display loading bar if recommendation is pending
            if st.session_state['recommended_language'] is None:
                with st.spinner('Generating recommended programming language...'):
                    text = st.session_state.get('requirements_text', '')
                    recommended_language = gpt_instance(input=f'Given these requirements:\n{text}\n Recommend a programming language to use based on simplicity of implementation and integrations out of the following languages: [{"".join(LANGUAGES)}]? Respond ONLY with ONE programming language and nothing else.', max_tokens=5).content
                    # Extract and update language choice
                    st.session_state['recommended_language'] = recommended_language
            # Allow user to select or change language
            options = LANGUAGES + [st.session_state['recommended_language']] if st.session_state['recommended_language'] not in LANGUAGES else LANGUAGES
            st.session_state['recommended_language'] = st.selectbox('', options, index=options.index(st.session_state['recommended_language']))

        # API framework selection
        col1_ts, col2_ts = st.columns([3, 5])
        with col1_ts:
            st.write("Selected API framework:")
        with col2_ts:
            if st.session_state['recommended_framework'] is None:
                with st.spinner('Generating recommended API framework...'):
                    # Assume requirements text is stored in session state
                    recommended_framework = gpt_instance(input=f'Given these requirements:\n{text}\n Given also that we are using this language:\n{recommended_language}\n Recommend an API framework to use based on simplicity of implementation, compatibility with requirements, and available integrations out of the following API frameworks: [{"".join(API_FRAMEWORKS)}]? Respond ONLY with ONE API framework and nothing else.', max_tokens=10).content
                    st.session_state['recommended_framework'] = recommended_framework
            options_framework = list(set(API_FRAMEWORKS + [st.session_state['recommended_framework']]))
            st.session_state['recommended_framework'] = st.selectbox('', options_framework, index=options_framework.index(st.session_state['recommended_framework']))

        # Database selection
        col1_db, col2_db = st.columns([3, 5])
        with col1_db:
            st.write("Selected database:")
        with col2_db:
            if st.session_state['recommended_database'] is None:
                with st.spinner('Generating recommended database...'):
                    recommended_db = gpt_instance(input=f'Given these requirements:\n{text}\n Given also that we are using this language {recommended_language} with this API framework {recommended_framework}, recommend a database to use based on simplicity of use, compatibility with requirements, language, and API framework, ease of use, popularity in developer community, efficiency, and scalability out of the following databases: [{"".join(DATABASES)}]? If the requirements do not require a database, choose the "None needed" option. Respond ONLY with ONE option and nothing else.', max_tokens=10).content
                    st.session_state['recommended_database'] = recommended_db
            options_db = list(set(DATABASES + [st.session_state['recommended_database']]))
            st.session_state['recommended_database'] = st.selectbox('', options_db, index=options_db.index(st.session_state['recommended_database']))

        # Integration selection
        col1_integration, col2_integration = st.columns([3, 5])
        with col1_integration:
            st.write("Selected additional integrations:")
        with col2_integration:
            if st.session_state['recommended_integrations'] is None:
                with st.spinner('Generating recommended integrations...'):
                    recommended_integrations = gpt_instance(input=f'Given these requirements:\n{text}\n Given also that we are using this language {recommended_language} with this API framework {recommended_framework} and this database {recommended_db}, recommend the MOST IMPORTANT integration to use that is necessary for building an application fullfilling the requirements out of these additional integrations: [{"".join(INTEGRATIONS)}]? If the requirements do not require an integration, choose the "None needed" option. Respond ONLY with ONE option and nothing else.', max_tokens=10).content
                    st.session_state['recommended_integrations'] = recommended_integrations
            options_integration = list(set(INTEGRATIONS + [st.session_state['recommended_integrations']]))
            st.session_state['recommended_integrations'] = st.selectbox('', options_integration, index=options_integration.index(st.session_state['recommended_integrations']))
        
        # Button to proceed to the next step, should be enabled only after all selections are made
        all_selections_made = all([
            st.session_state['recommended_language'] is not None,
            st.session_state['recommended_framework'] is not None,
            st.session_state['recommended_database'] is not None,
            st.session_state['recommended_integrations'] is not None
        ])
        if all_selections_made:
            submit_button = st.button("Step 3: Generate UML")
            if submit_button:
                # Perform next actions here such as generating UML and navigating to the next page
                pass