import streamlit as st
from funtion_database import change_password,add_new_user,delete_user
st.set_page_config(
    page_title="Account Management 🔑",
    page_icon="👋",
)
st.title("# ACCOUNT MANAGEMENT! 🔑")
st.header("CHANGE PASSWORD:")
username = st.text_input("Username")
password_old = st.text_input("Password old:", type="password")
password_new= st.text_input("Password new:", type="password")
if st.button("CHANGE PASSWORD"):
    # Check if the username and password are correct
    notice=change_password(username,password_old,password_new)
    st.write(notice)
try:
    if st.session_state.position!="staff":
        st.header("CREATE OR DELETE ACCOUNT:")
        if st.session_state.position=="master":
            list_type=["admin","staff"]
        else:
            list_type=['staff']
        type_acc=st.selectbox("Type Account:",list_type)
        username_=st.text_input("Username:")
        password_new_=st.text_input("Password:", type="password")
        row_butt=st.columns(4)
        with row_butt[0]:
            if st.button("CREATE ACCOUNT"):
                notice=add_new_user(username_,password_new_,type_acc)
                st.write(notice)
        with row_butt[1]:
            if st.button("DELETE ACCOUNT"):
                notice=delete_user(username_,type_acc)
                st.write(notice)
except:
    print()