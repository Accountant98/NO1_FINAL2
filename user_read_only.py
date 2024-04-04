import streamlit as st
import pandas as pd
from streamlit_extras.grid import grid
from read_data_view import *
from funtion_database import *
def reset_data():
    if st.session_state.get('data') is None:
        st.session_state['data'] = {}

def set_data(key: str,value):
    st.session_state['data'][key] = value

def get_data(key):
    return st.session_state['data'].get(key)

def user_read_only():
    #st.session_state['data'] = {}
    reset_data()
    #set_data("flag_view",0)
    # APP
    col_left, col_right = st.columns([1,3])
    with col_left:
        with st.form('input_form'):
            # PROJECT BOX
            col_left_prj_grid = grid(1,2,2,2,vertical_align="top")
            # Row 1:
            col_left_prj_grid.header("Project")
            # Row 2:
            col_left_prj_grid.text_input("Model Code", key="code")
            col_left_prj_grid.selectbox("PowerTrain",['EV', 'e-Power', 'ICE'],key="pwt")
            # Row 3:
            col_left_prj_grid.selectbox("Case",['CASE1', 'CASE1.5', 'CASE2'],key="case")
            col_left_prj_grid.selectbox("Plant",['JPN', 'US', 'EUR', 'PRC'],key="plant")
            # Row 4:
            col_left_prj_grid.selectbox("Dev",['ALL','XQ4', 'XR2', 'XR3'], key="dev")
            col_left_prj_grid.selectbox("Lot",["ALL",'DS', 'DC', 'PFC','VC','PT1','PT2'], key="lot")
            st.header("View Box")
            col_left_spec_grid = grid(1,vertical_align="top")
            if col_left_spec_grid.form_submit_button("View Data", use_container_width=True):
                with st.spinner(text="In progress..."):
                    list_file,folder_output,name_zip=check_file_out(st.session_state.code,st.session_state.pwt,st.session_state.plant,st.session_state.case)
                    set_data("folder_output",folder_output)
                    set_data("name_zip",name_zip)
                    session, data, project_id, app_list=query_data(st.session_state.code,st.session_state.plant,st.session_state.pwt,st.session_state.case,st.session_state.dev,st.session_state.lot)
                    set_data("data_cadics",data)
                    set_state_db(session,project_id,app_list)
                    list_link=["Car配車要望表","WTC仕様用途一覧表","WTC要望集約兼チェックリスト","実験部品","特性管理部品リスト","File Log.xlsx"]
                    for index in range(len(list_link)):
                        set_data(list_link[index],list_file[index])
                        set_data("flag_view",1)
                st.write("Completed!!!")
            #BANNER RIGHT
            with col_right:
                col_r1, col_r2 = st.columns([2,1])
                with col_r1:
                    st.markdown('<h1 style="text-align: center;">プロ管集約業務システム</h1>', unsafe_allow_html=True)

                with col_r2:
                    st.markdown(f'<p style="text-align: center;">{st.session_state.name_user}.</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: center;">{st.session_state.position}</p>', unsafe_allow_html=True)
                    
                view("staff")
                # Create button select output : Cadis or 5 output
                
def view(position):
    button_select_caout_grid = grid(2,1,4,vertical_align="top")
    row_butt=st.columns(6)   
    selected_option_output_select = button_select_caout_grid.selectbox("SELECT OUTPUT",["CADICS 項目","Car配車要望表","WTC仕様用途一覧表","WTC要望集約兼チェックリスト","実験部品","特性管理部品リスト","File Log"])
    # area for table output

    if get_data("flag_view") == 1:
        if selected_option_output_select == "CADICS 項目" :
            Sheet_name = button_select_caout_grid.selectbox("Select Sheet",["CADICS"])
            if position=="staff":
                button_select_caout_grid.dataframe(get_data("data_cadics"),height=525)
            if position!="staff":
                if  get_data("session")!=None:
                    data_edit=button_select_caout_grid.data_editor(get_data("data_cadics"),height=525)
                    with row_butt[3]:
                        if st.button("SAVE",use_container_width=True):
                            with st.spinner(text="In progress..."):
                                update_edit(data_edit,get_data("session"),get_data("data_cadics"),get_data("project_id"),get_data("app_list"))
                                set_data("data_cadics",data_edit)
                            st.write("Save Completed!!!")
                else:
                    button_select_caout_grid.dataframe(get_data("data_cadics"),height=525)

            set_data("link", "cadics")

        if selected_option_output_select == "Car配車要望表" :
            Sheet_name = button_select_caout_grid.selectbox("Select Sheet",["PFC","VC","PT1","PT2"])
            data=read_output(get_data("Car配車要望表"),Sheet_name)
            button_select_caout_grid.dataframe(data,height=525)
            set_data("link", get_data("Car配車要望表"))
            set_data("name", "Car配車要望表.xlsx")
            
        if selected_option_output_select == "WTC仕様用途一覧表" :
            Sheet_name = button_select_caout_grid.selectbox("Select Sheet",["PFC","VC"])
            data=read_output(get_data("WTC仕様用途一覧表"),Sheet_name)
            button_select_caout_grid.dataframe(data,height=525)
            set_data("link", get_data("WTC仕様用途一覧表"))
            set_data("name", "WTC仕様用途一覧表.xlsx")
    
        if selected_option_output_select == "WTC要望集約兼チェックリスト" :
            Sheet_name = button_select_caout_grid.selectbox("Select Sheet",["PFC","VC"])
            data=read_output(get_data("WTC要望集約兼チェックリスト"),Sheet_name)
            button_select_caout_grid.dataframe(data,height=525)
            set_data("link", get_data("WTC要望集約兼チェックリスト"))
            set_data("name", "WTC要望集約兼チェックリスト.xlsx")
    
        if selected_option_output_select == "実験部品" :
            Sheet_name = button_select_caout_grid.selectbox("Select Sheet",["PFC","VC"])
            data=read_output(get_data("実験部品"),Sheet_name)
            button_select_caout_grid.dataframe(data,height=525)
            set_data("link", get_data("実験部品"))
            set_data("name", "実験部品.xlsx")
    
        if selected_option_output_select == "特性管理部品リスト" :
            Sheet_name = button_select_caout_grid.selectbox("Select Sheet",["PFC","VC"])
            data=read_output(get_data("特性管理部品リスト"),Sheet_name)
            button_select_caout_grid.dataframe(data,height=525)
            set_data("link", get_data("特性管理部品リスト"))
            set_data("name", "特性管理部品リスト.xlsx")

        if selected_option_output_select == "File Log" :
            Sheet_name = button_select_caout_grid.selectbox("Select Sheet",["COUNT","関連表①","関連表②","関連表③","関連表④"])
            data=read_output(get_data("File Log"),Sheet_name)
            button_select_caout_grid.dataframe(data,height=525)
            set_data("link", get_data("File Log"))
            set_data("name", "File Log.xlsx")
    
        # button save and download
        button_select_caout_grid.header("")
        button_select_caout_grid.header("")
        with row_butt[4]:
            if get_data("link")!=None and get_data("link")!="cadics":
                with open(get_data("link"), "rb") as fp:
                    st.download_button(
                        label="Download File",
                        data=fp,
                        file_name=get_data("name"),
                        mime="text/plain",
                        use_container_width=True
                    )
            elif get_data("link")=="cadics" and len(get_data("data_cadics").columns)>31:
                    bool=st.download_button(
                        label="Download File",
                        data=get_data("data_cadics").to_csv(index=None,header=None),
                        file_name="CADICS_ALL.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                    if bool==True and position=="admin":
                        write_cadic_temp(st.session_state.name_user,position,st.session_state.code,st.session_state.pwt,
                                              st.session_state.plant,st.session_state.case,get_data("data_cadics"))
                        bool=False
        with row_butt[5]:
            try:
                #zip_folder(get_data("folder_output"),get_data("folder_output")+".zip")
                with open(get_data("folder_output")+".zip", "rb") as fp:
                    st.download_button(
                        label="Download All",
                        data=fp,
                        file_name=get_data("name_zip"),
                        mime="application/zip",
                        use_container_width=True
                    )
            except:
                None
    else:
        Sheet_name = button_select_caout_grid.selectbox("Select Sheet", [])
        data_empty = pd.DataFrame([[""] * 30] * 20)
        column_names = [f'{i + 1}' for i in range(30)]
        data_empty = pd.DataFrame(data_empty, columns=column_names)
        data_empty = data_empty.fillna("")
        button_select_caout_grid.dataframe(data_empty, height=525)


def set_state_db(session,project_id,app_list):
    set_data("session",session)
    set_data("project_id",project_id)
    set_data("app_list",app_list)
