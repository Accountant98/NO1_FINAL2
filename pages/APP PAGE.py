
import streamlit as st
from user_read_only import user_read_only
from admin import admin
st.set_page_config(
    page_title="My Streamlit App",
    page_icon=":smiley:",
    layout="wide"  
)
def reset_data():
    if st.session_state.get('data') is not None:
        st.session_state['data'] = {}

if 1==1:
    try :
        if st.session_state.position=="admin" or st.session_state.position=="master": #st.session_state.mail:
        #------------MAIN APP-----------x
            try:
    
                admin()
            except Exception as e:
                st.error(f"Error: {e}")
        elif st.session_state.position=="staff" :
            try:
                user_read_only()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please login before running app!!!")
    except:
        st.warning("Please login before running app!!!")
else:
    if st.session_state.position=="admin" or st.session_state.position=="master" : #st.session_state.mail:
        #------------MAIN APP-----------x
        admin()
    elif st.session_state.position=="staff" :
         user_read_only()