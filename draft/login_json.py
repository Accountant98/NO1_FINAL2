import streamlit as st
import json
import hashlib
#from sql import *

# BACK-END check ------------------------------------------------------
@st.cache_resource

def load_accounts_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:  # Sử dụng codec utf-8
        data = json.load(file)
    return data["accounts"]


def authenticate(username, password):
    JSON_FILE = r"data/list_acc.json"
    accounts = load_accounts_from_json(JSON_FILE)
    sha256_pass = hashlib.sha256(password.encode()).hexdigest()
    for account_type in accounts:
        for account in accounts[account_type]:
            if account.get("user") == username and account.get("password") == sha256_pass:
                return True, account.get("position") 
    return False, None




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
    check,position=authenticate(username, password)
    if check==True:
        st.session_state.position=position
        st.success("Login successful!")
    else:
        st.session_state.position=None
        st.error("Login failed. Please check your credentials.")


