import streamlit as st

st.set_page_config(page_title="Generate Design")

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

submit_button = st.button("Step 4: Generate Backend Code")
if submit_button:
    with st.spinner(" (4/4) generating Repo structure ..."):
        # TODO: pass the uml design, project requirements 
        # uml_dir_json = folder_structure_gen.folder_structure_gen(None, uml_dict["uml_code"])
        # st.session_state['uml_dir_json'] = uml_dir_json
        pass