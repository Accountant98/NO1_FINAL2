# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import openpyxl
import unicodedata
import os
import time
import json
from collections import OrderedDict
from merge_row_cadics import merge_row_cadics
import warnings
warnings.filterwarnings("ignore")
from check_zone import condition_zone_check
from check_option import check_option
from log_file_error import check_document
from funtion_database import update_new
from read_data_view import frame_empty

def create_cadics(case, market, powertrain, car):
    working = os.path.dirname(__file__)
    folder_name = str(car).upper() + "_" + powertrain + "_" + market + "_" + case
    folder_data=os.path.join(working, "data", str(car).upper())
    folder_data=folder_data.replace("\\","/")
    folder_out_check = os.path.join(working, "output", folder_name)
    folder_out_check = folder_out_check.replace("\\", "/")
    if os.path.exists(folder_out_check) == False:
        os.mkdir(folder_out_check)
    file_spec,dic_group_karenhyo12,notice=get_group_karenhyo12(folder_data,car,folder_out_check)
    if file_spec==None or len(dic_group_karenhyo12)==0:
        return "Check input again!!!",None,frame_empty(),None,None
    # ===========================set link output=============================
    #link_cadic = folder_out_check+"/"+ "CADICS_ALL.csv"

    my_dict_data = [{i: None for i in range(1, 180)}]
    data_spec = pd.read_excel(file_spec, sheet_name="Sheet1", header=None)

    data_spec = data_spec.applymap(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
    
    body_type=data_spec.iat[3,4]
    # ========================Create File Output=============================
    adddress_config, frame_header,dict_grade, max_car,dict_optioncode = get_infor_car(data_spec)
    dict_except_config = lot_except_config(data_spec)

    for group in dic_group_karenhyo12.keys():
        file_karenhyo_1=dic_group_karenhyo12[group][0]
        file_karenhyo_2=dic_group_karenhyo12[group][1]
        data_karenhyo1 = pd.read_excel(file_karenhyo_1, sheet_name="関連表", header=None)
        data_karenhyo1 = data_karenhyo1.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
        data_karenhyo1_list = data_karenhyo1.values
        max_column_karenhyo1 = len(data_karenhyo1.columns)

        data_karenhyo2 = pd.read_excel(file_karenhyo_2, sheet_name="関連表", header=None)
        data_karenhyo2 = data_karenhyo2.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
        dic_lot = get_lot(file_karenhyo_1, powertrain, market, case)  # contain
        flag_all,address_zone=condition_zone_check(data_karenhyo2,adddress_config)
        common_option,dict_kep=check_option(data_karenhyo2,file_spec)
        list_infor = get_infor_fixed_group(data_karenhyo2)
        # ========================================================================
        for lot in dic_lot.keys():
            batan_no = dic_lot[lot]
            list_cadics = get_list_cadic(batan_no, data_karenhyo1, data_karenhyo1_list, max_column_karenhyo1)
            list_cadics_filter=filter_cadics(data_karenhyo2,list_cadics,address_zone,body_type)
            if len(list_cadics_filter) > 0:
                for cadics_no in list_cadics_filter:
                    list_dic_records = pick_car(data_karenhyo2, dict_except_config, cadics_no, adddress_config,
                                                group,lot, data_spec, list_infor,address_zone,
                                                dict_grade,common_option,max_car,dict_optioncode,flag_all,dict_kep)
                    my_dict_data = my_dict_data + list_dic_records


    frame_data=edit_dataframe(my_dict_data, frame_header)
    session, data, project_id, app_list=update_new(str(car).upper(),market,powertrain,case,frame_data)
    return notice,session, data, project_id, app_list




def filter_cadics(data_karenhyo,list_cadic,address_zone,body):
    list_cadic_return=[]
    col_address_zone=[]
    dict_address_body ={"sdn":11,"h/b":12,"suv":13,"minivan":14,"frame":15}
    address_body=dict_address_body[body]
    
    for key in address_zone.keys():
        for item in address_zone[key]:
            if item[0] not in col_address_zone:
                col_address_zone.append(item[0])

    for cadic_no in list_cadic:
        address = data_karenhyo.loc[data_karenhyo[0] == cadic_no]
        col_pick = address.columns[address.eq("〇").any() | address.eq("○").any()]
        col_all_picked=[x for x in col_pick]
        col_zone_picked=list(set(col_all_picked).intersection(set(col_address_zone)))

        if len(col_zone_picked)!=0 and address_body in col_all_picked:
            list_cadic_return.append(cadic_no)

    return list_cadic_return

"""fuction:lot_except_config(data_spec):
-Description: get dic_except_config
-Input:data_spec (struct:dataframe)
-Output:dic_except_config (struct: {"DS":["config1","config2"],"DC":[],.....})
"""
def lot_except_config(data_spec):
    dic_except_config = {}
    list_lot = ["DS", "DC", "PFC", "VC", "PT1", "PT2"]
    for lot in list_lot:
        list_except = []
        lot=lot.lower()
        text_lot = lot + "-lot"
        address = data_spec.loc[data_spec[3] == text_lot]
        if address.empty:
            None
        else:
            col_pick = address.columns[address.eq("〇").any() | address.eq("○").any()]
            for index in col_pick:
                list_except.append(data_spec[index][0])
        dic_except_config[lot.upper()] = list_except
    return dic_except_config


"""fuction:get_lot(file_karenhyo_1,powertrain,market,case):
-Description: get all lot
-Input:file_karenhyo_1,powertrain,market,case
-Output:list_lot(struct:{key=lot:value=batan_no},Eg:{"DS":1,"DC":2...})
"""
def get_lot(file_karenhyo_1, powertrain, market, case):
    address_pwt = {"EV": 0, "e-Power": 10, "ICE": 20}
    address_maket_case = {"JPN_CASE1": 2, "US_CASE1.5": 3, "US_CASE2": 4, "PRC_CASE1.5": 5, "PRC_CASE2": 6,
                          "EUR_CASE1.5": 7, "EUR_CASE2": 8}
    list_lot_all = ["DS", "DC", "PFC", "VC", "PT1", "PT2"]
    dic_lot = {}
    df = pd.read_excel(file_karenhyo_1, sheet_name="パターン", header=None)
    data_batan = df.values
    market_case_in = market + "_" + case
    col_pwt = address_pwt[powertrain]
    row_maket_case = address_maket_case[market_case_in]
    col_lot_start = col_pwt + 3
    for lot in list_lot_all:
        batan_value = data_batan[row_maket_case][col_lot_start]
        if batan_value != "-" and isinstance(batan_value, (int, str)) == True:
            dic_lot[lot] = batan_value
        col_lot_start = col_lot_start + 1
    return dic_lot


# ============================================================================================
"""fuction:get_infor_fixed_group(data_karenhyo):
-Description: get inforation of file karenhyo2 
-Input:file_karenhyo_1,powertrain,market,case
-Output:list_infor (struct: [col_zone,row_option,row_item])
"""
def get_infor_fixed_group(data_karenhyo):
    max_col=len(data_karenhyo.columns)
    row_opt = data_karenhyo.iloc[1:2]
    row_item = data_karenhyo.iloc[2:3]
    row_class=data_karenhyo.iloc[3:4]
    col_zone_list = row_opt.columns[row_opt.eq("zone").any()]
    if len(col_zone_list):
        col_zone = col_zone_list[-1]
    else:
        col_zone=max_col
    return [col_zone, row_opt, row_item,row_class]

# =====================================================================================
"""fuction:get_list_cadic(batan_no,df,data_karenhyo,max_column_karenhyo):
-Description: get list_cadics 
-Input:batan_no,df,data_karenhyo,max_column_karenhyo
-Output:list_cadics(struct: ["MSTR-004-0000100","MSTR-004-0000200",...])
"""
def get_list_cadic(batan_no, df, data_karenhyo, max_column_karenhyo):
    column_batan = -1
    for index in range(11, max_column_karenhyo):
        if data_karenhyo[1][index] == batan_no:
            column_batan = index
            break
        
    if column_batan == -1:
        return []

    filtered_data = df.loc[
        df[0].notna() & df[0].apply(lambda x: isinstance(x, str)) & ((df[index] == "〇") | (df[index] == "○"))]
    cadic = filtered_data[0].tolist()
    return cadic


"""fuction:get_infor_car(df_spec):
-Description: get car's information 
-Input: df_spec
-Output: dic_col_config, frame_header, dict_grade,count,dict_optioncode
"""
def get_infor_car(df_spec):
    dict_grade={}
    dict_optioncode={}
    working = os.path.dirname(__file__)
    link_form_cadic=working+"/form_out/form_cadics.csv"
    link_form_cadic=link_form_cadic.replace("\\","/")
    frame_header = pd.read_csv(link_form_cadic, header=None)
    num_columns = len(frame_header.columns)
    column_names = [f'{i + 1}' for i in range(num_columns)]
    frame_header.columns = column_names
    dic_col_config = {}
    col_car_cadics = 130
    max_co = len(df_spec.columns)
    count=0
    row_opcode = df_spec.loc[df_spec[3] == "optioncode"].index[0]
    for index in range(4, max_co):
        config=df_spec[index][0]
        grade=df_spec[index][7]
        zone=df_spec[index][2]
        optioncode=df_spec[index][row_opcode]
    #==============================================fix zone=============================================
        if zone=="usa":
            zone="us"
        if zone=="canada":
            zone="can"
    #====================================================================================================
        if config != None and isinstance(config, float) == False:
            count=count+1
            if isinstance(optioncode,str):
                dict_optioncode[config]=optioncode
            else:
                dict_optioncode[config]=""

    #==================================lay cac cofig up_dow =============================================
            if zone not in dict_grade.keys():
                dic_col_config[zone]={config:col_car_cadics}
                dict_grade[zone]={config:grade}

            else:
                dict_grade[zone][config]=grade
                dic_col_config[zone][config]=col_car_cadics

            col_car_cadics = col_car_cadics + 1

    df_spec=df_spec.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    frame_car = df_spec.iloc[[2, 4, 8, 5, 6, 0], 4:(4 + count)]
    frame_car = frame_car.reset_index(drop=True)
    column_names = [f'{i}' for i in range(130, 130 + count)]
    frame_car.columns = column_names
    frame_header = pd.concat([frame_header, frame_car], axis=1)
    return dic_col_config, frame_header, dict_grade,count,dict_optioncode


"""fuction:copy_car(dic_opt):
-Description: Calculate required car config 
-Input: dic_opt: selected equipment
-Output: list car_config 
"""
def cal_option(dic_opt,codition_zone):
    list_car=[]
    list_old = [{}]
    list_new = [{}]
    for item in dic_opt.keys():
        list_old = list_new.copy()
        list_new = []
        for dic_sub in list_old:
            for op in dic_opt[item]:
                dic_sub2 = dic_sub.copy()
                dic_sub2[item] = op
                list_new.append(dic_sub2)

    for item in list_new:
        dic_car={}
        list_condition=[item[key][1] for key in item.keys()]
        list_condition.append(codition_zone)
        list_condition = list(OrderedDict.fromkeys(list_condition))
        if len(list_condition)==1:
            for key in item:
                dic_car[key]=item[key][0]
            dic_car["グレード選択"]=list_condition[0]
            list_car.append(dic_car)

        if len(list_condition)==2 and "不問" in list_condition:
            list_condition.remove("不問")
            for key in item:
                dic_car[key]=item[key][0]
            dic_car["グレード選択"]=list_condition[0]
            list_car.append(dic_car)

    return list_car


"""fuction: pick_car(data_karenhyo,dict_except_config,cadic_no,adddress_config,group,lot,data_spec,infor_fix)
-Description: pick 1,*
"""
def pick_car(data_karenhyo, dict_except_config, cadic_no, adddress_config, group, lot, data_spec, 
            infor_fix,address_zone,dict_grade,common_option,max_car,dict_optioncode,flag_all,dict_kep):
    col_zone, row_opt, row_item,row_class = infor_fix
    list_except_config = dict_except_config[lot]
    dic_address = {"DS": [55, 61, 67], "DC": [55, 68, 74], "PFC": [75, 81, 91], "VC": [92, 98, 107], "PT1": [92, 108, 117], "PT2": [92, 118, 127]}
    col_group, col_evaluate, col_comment = dic_address[lot]
    list_dict = []
    dic_data = {}
    # find  cadic of location in column A
    address = data_karenhyo.loc[data_karenhyo[0] == cadic_no]
    # find column picked 〇
    col_pick = address.columns[address.eq("〇").any() | address.eq("○").any()]
    col_all_picked=[x for x in col_pick]
    col_opt_pick = [x for x in col_pick if (x > col_zone)]
    
    index_cadic=0
    cadic_no_val=cadic_no.upper()
    for zone in address_zone.keys():
        if len(address_zone[zone])!=0:
            col_index_zone=[item[0] for item in address_zone[zone]]
            col_index_zone_picked=list(set(col_all_picked).intersection(set(col_index_zone)))
            if flag_all==True and len(address_zone[zone])>1:
                col_zone_all=col_index_zone[0]
                if col_zone_all in col_index_zone_picked:
                    col_index_zone_picked=[col_zone_all]

            for index in col_index_zone_picked:
                #===========finde condition zone=========
                for item in address_zone[zone]:
                    if item[0]==index:
                        condition_zone=item[1]
                        break
                #========================================
                adddress_cofig_zone,dict_grade_zone=get_config_zone(adddress_config,zone,dict_grade)
    # ===============Case haven't any 〇 picked======================================
                if len(col_opt_pick)==0:
                    dic_data=case_no_option(condition_zone,cadic_no_val,adddress_cofig_zone,group,
                                            col_group,col_evaluate,col_comment,dict_grade_zone,list_except_config)
                    if len(dic_data)>3:
                        list_dict.append(dic_data)
                        index_cadic=index_cadic+1
                        cadic_no_val=cadic_no.upper()+"-d000"+str(index_cadic)
                        
                else:
                    dict_opt=get_dict_option(col_opt_pick,row_opt,row_item,row_class,common_option)
                    list_car=cal_option(dict_opt,condition_zone)
                    list_all_config,list_car_fix=list_config_all_(list_car, data_spec, list_except_config,dict_grade_zone,common_option)
                    list_dict_data, index_cadic= case_have_option(list_all_config,list_car_fix,adddress_cofig_zone, 
                                                                  group,col_group,col_evaluate,
                                                                  col_comment,cadic_no,index_cadic,
                                                                  max_car,dict_optioncode,data_spec)
                    list_dict=list_dict+list_dict_data
    #================================================================================
                    
    if len(list_dict)==0:
        dic_data[2]=cadic_no.upper()
        dic_data[col_group]=group
        dic_data[col_evaluate]="YES"
        dic_data[130+max_car]="要望仕様が存在しない"
        dic_data[131+max_car]=comment_nashi(col_opt_pick,row_opt,row_item,row_class,dict_kep)
        return [dic_data]
    else:
        return list_dict


def comment_nashi(col_opt_pick,row_opt,row_item,row_class,dict_kep):  
    dic_opt = {}
    for index in col_opt_pick:
        opt = row_opt[index][1]
        opt=str(opt)
        opt=opt.strip()
        opt_item = row_item[index][2]
        opt_item=str(opt_item)
        opt_item=opt_item.strip()
        condition= row_class[index][3]
        if opt in dict_kep.keys():
            if isinstance(condition, str)==False:
                condition="不問"
            condition=condition.strip()
            if opt not in dic_opt.keys():
                dic_opt[opt] = []
            if condition not in ["最下級","最上級"]:
                condition="不問"

            if condition!="不問":
                string_comment="("+opt_item+", グレード選択:"+condition+")"
            else:
                string_comment=opt_item

            dic_opt[opt].append(string_comment)

    string_comment=str(dic_opt)
    for sym in ["{","}","[","]","'"]:
        string_comment=string_comment.replace(sym,"")

    return string_comment

def get_config_zone(adddress_config,zone,dict_grade):
    dict_config={}
    dict_grade_={}
    list_zone=zone.split("_")
    for item in list_zone:
        dict_config.update(adddress_config[item])
        dict_grade_.update(dict_grade[item])
    return dict_config, dict_grade_

def get_config_condition(condition_zone,dict_grade_):
    list_config=[]
    if condition_zone=="最上級":
        value_max = max(dict_grade_.values(),key=lambda x: str(x))
        for config in dict_grade_.keys():
            if dict_grade_[config]==value_max:
                list_config.append(config)

    if condition_zone=="最下級":
        value_min = min(dict_grade_.values(),key=lambda x: str(x))
        for config in dict_grade_.keys():
            if dict_grade_[config]==value_min:
                list_config.append(config)

    if condition_zone=="不問":
        for config in dict_grade_.keys():
            list_config.append(config)

    return list_config

def get_dict_option(col_opt_pick,row_opt,row_item,row_class,common_dict):
    dic_opt = {}
    for index in col_opt_pick:
        opt = row_opt[index][1]
        opt=str(opt)
        opt=opt.strip()
        opt_item = row_item[index][2]
        opt_item=str(opt_item)
        opt_item=opt_item.strip()
        condition= row_class[index][3]
        if isinstance(condition, str)==False:
            condition="不問"
        condition=condition.strip()
        sym_str=check_string(opt_item,2)
        if opt not in dic_opt.keys():
            dic_opt[opt] = []
        if condition not in ["最下級","最上級"]:
            condition="不問"

        list_item=common_dict[opt].copy()
        if sym_str=="all":
            for item in list_item:
                dic_opt[opt].append([item,condition])

        if sym_str in list_item:   
            dic_opt[opt].append([sym_str,condition])

        if sym_str=="w" and sym_str not in list_item:
            try:
                list_item.remove("w/o")
            except:
                None
            if len(list_item)>0:
                dic_opt[opt].append([sym_str,condition])       
    return dic_opt

def case_no_option(condition,cadic_no_val, address_config_zone, group,
                   col_group,col_evaluate,col_comment,dict_grade_zone,list_except_config):
    dic_data = {}
    flag_ = 0
    flag_2 = 0
    list_config_all=get_config_condition(condition,dict_grade_zone)
    if len(list_except_config)==0:
        list_config=list_config_all
    else:
        list_config=list(set(list_config_all).intersection(set(list_except_config)))
        
    list_config=sorted(list_config)
    for config in list_config:
        if flag_ == 0:
            dic_data[2] = cadic_no_val
            dic_data[col_group] = group
            dic_data[col_evaluate] = "YES"
            dic_data[address_config_zone[config]] = "1"
            if condition!="不問":
                dic_data[col_comment] = "グレード選択: "+condition
            flag_2 = 1
        if flag_ == 1:
            dic_data[address_config_zone[config]] = "*"
        if flag_2 == 1:
            flag_ = 1
    return dic_data
                  
def case_have_option(list_all_config,list_car,address_config_zone,
                      group,col_group,col_evaluate,
                      col_comment,cadic_no,index_cadic,
                      max_car,dict_optioncode,data_spec):

    list_dict=[]
    for index in range(len(list_all_config)):
        if len(list_all_config[index])!=0:
            dic_data = {}
            if index_cadic==0:
                dic_data[2] = cadic_no.upper()
            else:
                dic_data[2] = cadic_no.upper()+"-d000"+str(index_cadic)
            index_cadic=index_cadic+1
            dic_data[col_group] = group
            dic_data[col_evaluate] = "YES"
            dict_option=list_car[index]
            flag=0
            for config in list_all_config[index]:
                if flag==0:
                    dic_data[address_config_zone[config]]="1"
                    cmt=comment(dict_optioncode,config,dict_option,data_spec,max_car)

                    flag=1
                else:
                    dic_data[address_config_zone[config]]="*"
            dic_data[col_comment]=cmt
            list_dict.append(dic_data)

    return list_dict, index_cadic

def comment(dict_optioncode,config,dict_option,data_spec,max_car):
    for opt in dict_option.keys():
        if opt!="グレード選択":
            dict_option[opt]=list(dict.fromkeys(dict_option[opt]))      
    cmt=str(dict_option)

    if dict_optioncode[config]=="":
        for sys in ["{","}","'",", グレード選択: 不問","[","]"]:
            cmt=cmt.replace(sys,"")
        return cmt
    else:
        optioncode_config=dict_optioncode[config]
        for key in dict_option.keys():
            if key !="グレード選択":
                row_opcode = data_spec.loc[data_spec[3] == key].index[0]
                value=data_spec[4+max_car][row_opcode]
                if isinstance(value,str)==True and optioncode_config.find(value)!=-1:
                    cmt=cmt.replace("'"+key+"': "+str(dict_option[key]),value+":"+key+": "+str(dict_option[key]))
        
        for sys in ["{","}","'",", グレード選択: 不問","[","]"]:
            cmt=cmt.replace(sys,"")
        return cmt
            

def list_config_all_(car_list, data_spec, list_config_lot,dict_grade_zone,common_option):
    dict_index_option={}
    list_config_all = []   
    for car in car_list:
        car_ref=car.copy()
        condition=car["グレード選択"]
        del car_ref["グレード選択"]
        list_col = []
        flag=0
        if len(list_config_lot)==0:
            list_config_check=get_config_condition(condition,dict_grade_zone)
        else:
            list_config_condition=get_config_condition(condition,dict_grade_zone)
            list_config_check=list(set(list_config_lot).intersection(set(list_config_condition)))
      
        for opt in car_ref.keys():
            car[opt]=[]
            list_sub=[]
            address = data_spec.loc[data_spec[3] == opt]
            try:
                dict_index_option[opt]=address.index[0]
            except:
                None
            check_word=check_string(car_ref[opt],1,common_option[opt])
            for word in check_word:
                col_pick = address.columns[address.eq(word).any()]
                if len(col_pick) !=0:
                    list_temp=[x for x in col_pick]
                    list_sub=list_sub+list_temp

            if flag == 0:
                list_col = list_sub
                flag=1
            else:
                list_col = list(set(list_col).intersection(set(list_sub)))

        list_config = []
        for index in list_col:
            config=data_spec.iat[0,index]
            if config in list_config_check:
                list_config.append(config)
                for opt in dict_index_option.keys():
                    car[opt].append(data_spec.iat[dict_index_option[opt],index])

        list_config=sorted(list_config)
        list_config_all.append(list_config)

    return list_config_all,car_list



"""write_excel(my_dic_data,file_name,frame_header):
-Description: get config suiable for required config
-Input: my_dic_data,file_name,frame_header
-Output: write data in file csv
"""
def edit_dataframe(my_dic_data, frame_header):
    frame = pd.DataFrame(my_dic_data)
    frame = frame.drop(0)
    num_columns = len(frame.columns)
    column_names = [f'{i + 1}' for i in range(num_columns)]
    frame.columns = column_names
    df_sorted = frame.sort_values(by="2")
    result = pd.concat([frame_header, df_sorted], axis=0)
    # result.to_csv(file_name, index=False, header=None)
    result=result.reset_index(drop=True)
    result = pd.DataFrame(result.values, columns=None)
    data_new=merge_row_cadics(result)
    return data_new


def save_infor_json(file_path, my_dict):
    with open(file_path, 'w') as file:
        json.dump(my_dict, file)


def check_string(string,flag,list_item_opt=None):
    super_dic = {"w/o":['w/o','-'], "awd":["awd","4wd"], "fwd":["fwd","2wd"],"w":["w","with"]}
    if flag==1:
        if string!="w":
            for key in super_dic.keys(): 
                if string in super_dic[key]:
                    return super_dic[key]
            return [string]
        else:
            try:
                list_item=list_item_opt.copy()
                list_item.remove("w/o")
            except:
                None
            return list_item
    else:
        for key in super_dic.keys():
            if string in super_dic[key]:
                return key
        return string

def normalize_japanese_text(input_text):
    normalized_text = ''
    if isinstance(input_text,str):
        for char in input_text:
            normalized_char = unicodedata.normalize('NFKC', char)
            normalized_text += normalized_char
        normalized_text=normalized_text.replace("\n","")
        normalized_text=normalized_text.strip()
        return normalized_text
    else:
        return input_text


def get_group_karenhyo12(folder_data,car,folder_out):
    dic_group_karenhyo12={}
    if os.path.exists(folder_data)==False:
        return None, dic_group_karenhyo12
    files = [f for f in os.listdir(folder_data) if os.path.isfile(os.path.join(folder_data, f))]
    file_name_spec="仕様表_"+str(car).upper()+".xlsx"
    link_file_spec=os.path.join(folder_data,file_name_spec)
    link_file_spec=link_file_spec.replace("\\","/")
    notice=check_document(folder_data,link_file_spec,folder_out)
    if os.path.exists(link_file_spec)==False:
        link_file_spec=None

    for file_name in files:
        if file_name.find("関連表1")==0:
            file_karenhyo2=file_name.replace("関連表1","関連表2")
            link_file_karenhyo2=os.path.join(folder_data,file_karenhyo2)
            link_file_karenhyo2=link_file_karenhyo2.replace('\\','/')
            if os.path.exists(link_file_karenhyo2):
                link_file_karenhyo1=os.path.join(folder_data,file_name)
                link_file_karenhyo1=link_file_karenhyo1.replace('\\','/')
                dic_group_karenhyo12[file_name]=[link_file_karenhyo1,link_file_karenhyo2]

    return link_file_spec,dic_group_karenhyo12,notice
