# pages/generate_design.py
import streamlit as st
from function import uml, class_diagram
from function import folder_structure_gen

def app():
    col1, col2 = st.columns(2)
    st.subheader('UML Diagram')
    # retrieve uml_dict from session state
    dev_pref_lang = st.session_state.get('recommended_language', None)
    dev_pref_ts = st.session_state.get('recommended_framework', None)
    dev_pref_db = st.session_state.get('recommended_database', None)
    dev_pref_integration = st.session_state.get('recommended_integrations', None)
    project_req = st.session_state.get('requirements_text', None)

    placeholder = st.empty()

    with placeholder.container():
        st.write("(example output) ... waiting for UML generation ...")
        st.image(image='static/uml_demo.png', width=750)

        st.subheader('Class Diagram')
        st.write("(example output) ... waiting for class generation ...")
        st.image(image='static/class_demo.png', width=750)

        uml_dict = uml.generate_uml_code(project_req, 
                                        dev_pref_lang, dev_pref_ts, dev_pref_db, dev_pref_integration)
        st.session_state['uml_dict'] = uml_dict

    with placeholder.container():
        if uml_dict is not None:
            st.write(uml_dict["comments"])
            st.image(image=uml_dict["url"], width=750)
            st.markdown(
                    f'<a href="{uml_dict["url"]}" target="_blank"><input type="button" value="load uml"></a>',
                    unsafe_allow_html=True
                    )
    

    with placeholder.container():
        st.write(uml_dict["comments"])
        st.image(image=uml_dict["url"], width=750)
        st.markdown(
                f'<a href="{uml_dict["url"]}" target="_blank"><input type="button" value="load uml"></a>',
                unsafe_allow_html=True
                )
        st.subheader('Class Diagram')
        st.write("(example output) ... waiting for user description ...")
        st.image(image='static/class_demo.png', width=750)
        class_diagram_dict = class_diagram.generate_class_diagram_code(project_req, 
                                    dev_pref_lang, dev_pref_ts, dev_pref_db, dev_pref_integration)
        st.session_state['class_diagram_dict'] = class_diagram_dict

    with placeholder.container():
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

    submit_button = st.button("Step 4: Generate Backend Code")
    if submit_button and class_diagram_dict:
        with st.spinner(" (4/4) generating Repo structure ..."):
            uml_dir_json = folder_structure_gen.folder_structure_gen(project_req, 
                                                                     st.session_state.get('recommended_language'), uml_dict["uml_code"])
            st.session_state['current_page'] = 'Generate Backend'
            st.session_state['uml_dir_json'] = uml_dir_json
            st.switch_page('pages/generate_backend.py')