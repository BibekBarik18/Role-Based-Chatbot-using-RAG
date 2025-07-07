import streamlit as st



st.title("Role based chatbot using Rag")
option = st.selectbox(
    "Which department do you work in?",
    ("Engineer","Marketing","HR","Finance"),
)

if st.button("Chat", type="secondary"):
    if option:
        st.session_state.role_type=option
        st.switch_page("pages/chat.py")
    else:
        st.error("Please select a role to chat")

if st.button("Add another user",type="secondary"):
    st.switch_page("pages/add_user.py")

