import streamlit as st
import os
import base64
import secrets
import pandas as pd
from funtion_database import offline_edit
@st.cache_resource
def get_csrf_token():

    return base64.b64encode(secrets.token_bytes(32)).decode("utf-8")


def update_file_into_server(car_name, List_file, csrf_token):
    if csrf_token != get_csrf_token():
        st.error("Invalid CSRF token. This request is not allowed.")
        return
    if car_name!="" :
        car_name=str(car_name).upper()
        folder_save_file_upload = os.path.join('data', car_name)
        if not os.path.exists(folder_save_file_upload):
            os.makedirs(folder_save_file_upload)
        for file in List_file:
            file_path = os.path.join(folder_save_file_upload, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getvalue())
        if len(List_file)!=0:
            st.write("Update File Completed!!!")

def update_file_after_edit(code, pwt, plant, case, file_updates, csrf_token,name_user):
    flag=0
    if csrf_token != get_csrf_token():
        #st.error("Invalid CSRF token. This request is not allowed.")
        return "Invalid CSRF token. This request is not allowed."
    for file_update in file_updates:
        if file_update.name == "CADICS_ALL.csv":
            flag=1
            if code != "" and code!=None:
            #try:
                new_data=pd.read_csv(file_update,header=None)
                folder_name =str(name_user).upper() +"_"+ str(code).upper() + "_" + str(pwt).upper() + "_" + str(plant).upper() + "_" + str(case).upper()
                folder_save_file_update = os.path.join('cadic_temp', folder_name,"CADICS_ALL.csv")
                # st.warning(folder_save_file_update)
                if not os.path.exists(folder_save_file_update):
                    return "FAIL: There is no cadic references"
                else:
                    old_data=pd.read_csv(folder_save_file_update,header=None)
                    offline_edit(str(code).upper(), plant, pwt, case,new_data,old_data)
                    return "Update Completed!!!"

            # except:
            #     return "FAIL: ERROR CADICS_ALL.csv!!!"
                
            else:
                return "Project not exist!!!"
    if flag==0:
        return "FAIL: Files not CADICS_ALL.csv!!!"
