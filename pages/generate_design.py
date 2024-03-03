# pages/generate_design.py
import streamlit as st
from function import uml, class_diagram
from function import folder_structure_gen

def handle_button_click():
    st.session_state['submistted'] = True
    st.session_state['current_page'] = 'Generate Backend'

def app():
    # retrieve uml_dict from session state
    if 'submistted' not in st.session_state:
        st.session_state.submistted = False

    if st.session_state['submistted']:
        return

    dev_pref_lang = st.session_state.get('recommended_language', None)
    dev_pref_ts = st.session_state.get('recommended_framework', None)
    dev_pref_db = st.session_state.get('recommended_database', None)
    dev_pref_integration = st.session_state.get('recommended_integrations', None)
    project_req = st.session_state.get('requirements_text', None)

    placeholder = st.empty()

    with placeholder.container():
        st.subheader('UML Diagram')
        with st.spinner("Generating UML diagram ..."):
            st.write("(example output) ... waiting for UML generation ...")
            st.image(image='static/uml_demo.png', width=750)

            st.subheader('Class Diagram')
            st.write("(example output) ... waiting for class generation ...")
            st.image(image='static/class_demo.png', width=750)
            st.image(image='static/padding.png', width=750)
            st.image(image='static/padding.png', width=750)

            uml_dict = uml.generate_uml_code(project_req, 
                                            dev_pref_lang, dev_pref_ts, dev_pref_db, dev_pref_integration)
            st.session_state['uml_dict'] = uml_dict
            st.success

    with placeholder.container():
        st.subheader('UML Diagram')
        if uml_dict is not None:
            st.write(uml_dict["comments"])
            st.image(image=uml_dict["url"], width=750)
            st.markdown(
                    f'<a href="{uml_dict["url"]}" target="_blank"><input type="button" value="load uml"></a>',
                    unsafe_allow_html=True
                    )
    

    with placeholder.container():
        st.subheader('UML Diagram')
        st.write(uml_dict["comments"])
        st.image(image=uml_dict["url"], width=750)
        st.markdown(
                f'<a href="{uml_dict["url"]}" target="_blank"><input type="button" value="load uml"></a>',
                unsafe_allow_html=True
                )
        st.subheader('Class Diagram')
        with st.spinner("Generating class diagram ..."):
            st.write("(example output) ... waiting for user description ...")
            st.image(image='static/class_demo.png', width=750)
            st.image(image='static/padding.png', width=750)
            st.image(image='static/padding.png', width=750)
            class_diagram_dict = class_diagram.generate_class_diagram_code(project_req, 
                                        dev_pref_lang, dev_pref_ts, dev_pref_db, dev_pref_integration)
            st.session_state['class_diagram_dict'] = class_diagram_dict
            st.success

    with placeholder.container():
        st.subheader('UML Diagram')
        if class_diagram_dict is not None:
            st.write(uml_dict["comments"])
            st.image(image=uml_dict["url"], width=750)
            st.markdown(
                    f'<a href="{uml_dict["url"]}" target="_blank"><input type="button" value="load uml"></a>',
                    unsafe_allow_html=True
                    )
            st.subheader('Class Diagram')
            st.write(class_diagram_dict["comments"])
            st.image(image=class_diagram_dict["url"], width=750)
            st.markdown(
                f'<a href="{class_diagram_dict["url"]}" target="_blank"><input type="button" value="load uml"></a>',
                unsafe_allow_html=True
                )

        st.session_state.uml_code = uml_dict["uml_code"]
        st.session_state.project_req = project_req
        st.button("Step 4: Generate Backend Code", handle_button_click)
        st.image(image='static/padding.png', width=750)
        st.image(image='static/padding.png', width=750)