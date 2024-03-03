# pages/generate_backend.py
import streamlit as st
from templates import display_folder_structure
from function import folder_structure_gen
from function import endpoint_gen

import time
import json

def app():

    st.subheader('Backend Code and Folder Structure')
    with st.spinner("Generating Repo structure ..."):
        uml_dir_json = folder_structure_gen.folder_structure_gen(st.session_state.get('project_req'), st.session_state.get('recommended_language'), st.session_state.get('uml_code'))
        st.success()

    uml_dict_session_state = uml_dir_json
    dev_project_req = st.session_state.get('requirements_text', None)
    uml_dict = st.session_state.get('uml_dict', None)
    class_diagram_dict = st.session_state.get('class_diagram_dict', None)
    language = st.session_state.get('recommended_language', None)

    if uml_dict_session_state is not None:
        uml_dict_session_state = uml_dir_json
        display_folder_structure.display_tree(uml_dict_session_state, ["root"])

        gen_pseudo_buttom = st.button(
            "Approve folder structure and generate pseudo code")
        if gen_pseudo_buttom:
            with st.spinner("Generating pseudo code in repo ..."):
                pseudo_code_json = endpoint_gen.endpoint_generation(
                    dev_project_req, uml_dict['uml_code'], class_diagram_dict['uml_code'], language, uml_dict_session_state)
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
            
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.download_button(
                    data=folder_structure_gen.download_repo(
                        pseudo_code_json['endpoints']),
                    label="Download Repository",
                    file_name="generated_repo.zip",
                    mime="application/zip",
                    on_click=folder_structure_gen.download_repo,
                    args=(pseudo_code_json['endpoints'],)
                )
            with col2:
                st.button("Deploy Backend Code")
            with col3:
                st.button("Generate Postman Collection")
            with col4:
                st.button("Generate API Docs")
        else:
            st.write("... start pseudo code generation ...")

    else:
        st.write("(example output) ... waiting for user description ...")
        example_uml = """ 
            {"root": {"transcript_dataset": {"init.py": {}, "data_processing.py": {}, "tests": {"init.py": {}, "test_data_processing.py": {}}}, "language_model": {"init.py": {}, "model.py": {}, "preprocessing.py": {}, "tests": {"init.py": {}, "test_model.py": {}}}, "summarization_module": {"init.py": {}, "summarizer.py": {}, "tests": {"init.py": {}, "test_summarizer.py": {}}}, "key_point_extraction_module": {"init.py": {}, "extractor.py": {}, "tests": {"init.py": {}, "test_extractor.py": {}}}, "config": {"settings.py": {}}, "README.md": {}}}
                    """
        data = json.loads('{"root": {"transcript_dataset": {"init.py": {}, "data_processing.py": {}, "tests": {"init.py": {}, "test_data_processing.py": {}}}, "language_model": {"init.py": {}, "model.py": {}, "preprocessing.py": {}, "tests": {"init.py": {}, "test_model.py": {}}}, "summarization_module": {"init.py": {}, "summarizer.py": {}, "tests": {"init.py": {}, "test_summarizer.py": {}}}, "key_point_extraction_module": {"init.py": {}, "extractor.py": {}, "tests": {"init.py": {}, "test_extractor.py": {}}}, "config": {"settings.py": {}}, "README.md": {}}}')
        display_folder_structure.display_tree(data, ["root"])




    # if submit_button:
    #     with st.spinner(" (4/4) generating Repo structure ..."):
    #         # TODO: pass the uml design, project requirements 
    #         # uml_dir_json = folder_structure_gen.folder_structure_gen(None, uml_dict["uml_code"])
    #         # st.session_state['uml_dir_json'] = uml_dir_json
    #         pass