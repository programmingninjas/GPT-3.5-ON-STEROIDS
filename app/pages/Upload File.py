import streamlit as st

st.title("File Uploader for Analysis")

uploaded_file = st.file_uploader("If you want to analyse a file upload it before entering the task, Else ignore",type=["pdf","docx","xlsx","png","csv"])

if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None

if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file