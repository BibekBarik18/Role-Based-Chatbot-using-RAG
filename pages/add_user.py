import streamlit as st
from utils.partition import embed_documents


st.title("Add another role")
role = st.text_input("Role Name")
file = st.file_uploader("Upload the file to be embedded",type=["md"])
if file and role:
    if st.button("Embed Document"):
        with st.spinner("Embedding document..."):
            embed_documents(file,role)
        st.success("Document embedded successfully!")