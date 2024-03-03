# pages/landing_page.py
import streamlit as st
from function import uml
from function import folder_structure_gen

st.set_page_config(page_title="Choose Tech Stack")
###### Body ###############################################################################################################################
ui_block, uml_block = st.columns([0.7, 0.3])

#### user inputs ########
with ui_block:
    st.subheader("Choose Tech Stack")

    # developer's preference
    col1_lang, col2_lang = st.columns([3, 5])
    with col1_lang:
        st.write("")
        st.write('Preferred programming language?')
    with col2_lang:
        dev_pref_lang = st.selectbox('', ("No specific preference", "Python", "JavaScript", "Java", "Ruby", "C#", "Go", "PHP", "Swift", "TypeScript", "C++", "other"))
        if dev_pref_lang == "other":
            dev_pref_lang = st.text_input("")

    col1_ts, col2_ts = st.columns([3, 5])
    with col1_ts:
        st.write("")
        st.write("Preferred tech stack?")
    with col2_ts:
        dev_pref_ts = st.selectbox('', ("No specific preference",
                                                                    "MEAN (MongoDB, Express.js, Angular, Node.js)",
                                                                    "MERN (MongoDB, Express.js, React, Node.js)",
                                                                    "LAMP (Linux, Apache, MySQL, PHP/Python/Perl)",
                                                                    "Django (Python web framework with SQLite/PostgreSQL/MySQL)",
                                                                    "Ruby on Rails (Ruby web framework with SQLite/PostgreSQL/MySQL)",
                                                                    "ASP.NET (Microsoft's web framework with C# and SQL Server)",
                                                                    "Serverless (AWS Lambda, Azure Functions, Google Cloud Functions)",
                                                                    "JAMstack (JavaScript, APIs, Markup)",
                                                                    "PERN (PostgreSQL, Express.js, React, Node.js)",
                                                                    "Docker, Nginx, Flask, PostgreSQL (DNFP)",
                                                                    "Vue.js, Firebase, Firestore, Node.js (VFFN)",
                                                                    "MEVN (MongoDB, Express.js, Vue.js, Node.js)",
                                                                    "Laravel (PHP web framework with MySQL/PostgreSQL/SQLite)",
                                                                    "Spring Boot (Java web framework with Spring, Hibernate, and MySQL/PostgreSQL/Oracle)",
                                                                    "GraphQL, Apollo, React, Node.js (GARN)",
                                                                    "Flutter, Firebase, Cloud Firestore (FFCF)",
                                                                    "WordPress (PHP content management system with MySQL)",
                                                                    "Ionic, Angular, Firebase (IAF)",
                                                                    "Elastic Stack (Elasticsearch, Logstash, Kibana)",
                                                                    "Rust, Rocket (Rust web framework with PostgreSQL/MySQL)",
                                                                    "Phoenix (Elixir web framework with PostgreSQL/MySQL)",
                                                                    "Flask (Python micro web framework)",
                                                                    "Pyramid (Python web framework)",
                                                                    "FastAPI (Fast web framework for building APIs with Python)",
                                                                    "Dash (Python framework for building analytical web applications)",
                                                                    "Streamlit (Python library for building interactive web applications for data science)",
                                                                    "other"))
        if dev_pref_ts == "other":
            dev_pref_ts = st.text_input("")

    col1_db, col2_db = st.columns([3, 5])
    with col1_db:
        st.write("")
        st.write("Preferred database?")
    with col2_db:
        dev_pref_db = st.selectbox('', ("N/A", "MySQL", "MongoDB", "PostgreSQL", "SQLite", "Oracle", "Redis", "Cassandra", "Microsoft SQL Server",
                                                        "Amazon Aurora", "MariaDB", "Amazon DynamoDB", "Couchbase", "Firebase Realtime Database", "Google BigQuery", 
                                                        "InfluxDB", "Neo4j", "ArangoDB", "Apache HBase", "IBM Db2", "CouchDB", "No specific preference", "other"))
        if dev_pref_db == "other":
            dev_pref_db = st.text_input("")

    col1_integration, col2_integration = st.columns([3, 5])
    with col1_integration:
        st.write("")
        st.write("Add integration?")
    with col2_integration:
        dev_pref_integration = st.selectbox('', ("N/A","Stripe (Payment Gateway)", "PayPal (Payment Gateway)", "Braintree (Payment Gateway)",  "Google Maps API",
                                                        "Twitter API", "Facebook Graph API", "OAuth 2.0", "JSON Web Tokens (JWT)", "OpenID Connect", "Amazon Web Services (AWS)",
                                                        "Microsoft Azure", "Google Cloud Platform", "Salesforce API", "Twilio API", "Slack API", "Shopify API", "LinkedIn API",
                                                        "Mailchimp API", "Twitch API", "GitHub API", "more"))
        
        if dev_pref_integration == "more":
            dev_pref_integration = st.text_input("")
    
    submit_button = st.button("Submit")
    if submit_button:
        with st.spinner(" (2/2) generating UML and Repo structure ..."):
            # TODO: pass the uml design, project requirements 
            # uml_dir_json = folder_structure_gen.folder_structure_gen(None, uml_dict["uml_code"])
            # st.session_state['uml_dir_json'] = uml_dir_json
            pass
