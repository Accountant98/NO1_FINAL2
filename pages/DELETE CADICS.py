import streamlit as st
from streamlit_extras.grid import grid
from funtion_database import delete_project
def main():
    with st.form('input_form'):
        # Row 1:
        col_left_prj_grid = grid(1,2,2,2,vertical_align="top")
        col_left_prj_grid.header("Project")
        # Row 2:
        code=col_left_prj_grid.text_input("Model Code")
        pwt=col_left_prj_grid.selectbox("PowerTrain",['EV', 'e-Power', 'ICE'])
        # Row 3
        case= col_left_prj_grid.selectbox("Case",['CASE1', 'CASE1.5', 'CASE2'])
        plant=col_left_prj_grid.selectbox("Plant",['JPN', 'US', 'EUR', 'PRC'])
        # Row 4:
        row_butt=st.columns(3)
        if row_butt[1].form_submit_button("DELETE IN DB", use_container_width=True):
            with st.spinner(text="In progress..."):
                notice=delete_project(code,plant,pwt,case)
            st.write(notice)


if __name__ == "__main__":
    try:
        if st.session_state.position!="staff":
            main()
        else:
            st.warning("Permission Deny!")
    except:
        st.warning("Please login before running app!!!")
