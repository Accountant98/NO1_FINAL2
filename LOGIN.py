import streamlit as st
from funtion_database import log_in
#from sql import *
# BACK-END check ------------------------------------------------------
# --------------------------------- GAMEN -------------------------------

st.set_page_config(
    page_title="Login Page",
    page_icon="👋",
)
st.header("# Welcome to system XQA_プロ管集約業務の一本化 ! 👋")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    # Check if the username and password are correct
    name_user,position,project_query=log_in(username, password)
    if position!=None:
        st.session_state.position=position
        st.session_state.name_user=name_user
        st.session_state.project_query=project_query
        st.success("Login successful!")
        st.switch_page("pages/APP PAGE.py")
    else:
        st.session_state.position=None
        st.error("Login failed. Please check your credentials.")


