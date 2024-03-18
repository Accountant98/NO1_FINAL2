import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, update, func
from sqlalchemy.orm import sessionmaker, aliased, declarative_base
import streamlit as st
import numpy as np

Base = declarative_base()

class Header(Base):
    __tablename__ = 'header'
    id = Column(Integer, primary_key=True)
    id_project = Column(Integer, ForeignKey('project.id_project'))
    for i in range(1, 130):
        locals()[f'col{i}'] = Column(String)

class Project(Base):
    __tablename__ = 'project'
    id_project = Column(Integer, primary_key=True)
    project_name = Column(String)
    power_train = Column(String)
    market = Column(String)
    develop_case = Column(String)


class App(Base):
    __tablename__ = 'app'
    id_app = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id_project'))
    market = Column(String)
    engine = Column(String)
    gearbox = Column(String)
    axle = Column(String)
    handle = Column(String)
    app = Column(String)

columns = ['action','cadic_number','snt','regulations','pep','Other','good_design','y0','y0_number','car_recurrence_prevention','solution','solution_number','common_validation_item','procedure_item','requirement','step1_pt_jp','step2_pt_jp','step1_vt_jp','step2_vt_jp','step3_vt_jp','lv1_ct_jp','lv2_ct_jp','lv3_ct_jp','lv4_ct_jp','comment_ct_jp','step1_pt_en','step2_pt_en','step1_vt_en','step2_vt_en','step3_vt_en','lv1_ct_en','lv2_ct_en','lv3_ct_en','lv4_ct_en','comment_ct_en','digital_evaluation_app','pf_evaluation_app','physical_evaluation_app','kca_project_group_deploy','team_deploy','manager_name_deploy','id_or_mail_account_deploy','name_of_person_in_charge_deploy','id_or_mail_account_2_deploy','target_value_deploy','comment_deploy','kca_project_group_ac','team_ac','manager_name_ac','id_or_mail_account_ac','name_of_person_in_charge_ac','id_or_mail_account_2_ac','agreement_of_target_ac','comment_ac','kca_project_group_digital','team_digital','manager_name_digital','id_or_mail_account_digital','evaluation_responsible_digital','id_or_mail_account_2_digital','evaluate_or_not_ds','result_first_ds','report_number_ds','number_of_qbase_ds','qbase_number_ds','result_counter_ds','comment_ds','evaluate_or_not_dc','result_first_dc','report_number_dc','number_of_qbase_dc','qbase_number_dc','result_counter_dc','comment_dc','kca_project_group_ppc','team_ppc','manager_name_ppc','id_or_mail_account_ppc','evaluation_responsible_ppc','id_or_mail_account_2_ppc','evaluate_or_not_pfc','confirmation_first_pfc','feedback_timing_pfc','result_first_pfc','confirmation_completion_pfc','report_number_pfc','number_of_qbase_pfc','qbase_number_pfc','result_counter_pfc','confirmation_completion_date_pfc','comment_pfc','kca_project_group_ppe','team_ppe','manager_name_ppe','id_or_mail_account_ppe','evaluation_responsible_ppe','id_or_mail_account_2_ppe','evaluate_or_not_vc','confirm_first_date_vc','result_first_vc','confirm_first_completion_vc','report_number_vc','number_of_qbase_vc','qbase_number_vc','result_counter_vc','confirm_first_completion_2_vc','comment_vc','evaluate_or_not_pt1','confirm_first_date_pt1','result_first_pt1','confirm_first_completion_pt1','report_number_pt1','number_of_qbase_pt1','qbase_number_pt1','result_counter_pt1','confirm_first_completion_2_pt1','comment_pt1','evaluate_or_not_pt2','confirmation_first_time_pt2','result_first_pt2','confirm_first_completion_pt2','report_number_pt2','number_of_qbase_pt2','qbase_number_pt2','result_counter_pt2','confirm_first_completion_2_pt2','comment_pt2','common_unique']
class MainTable(Base):
    __tablename__ = 'main_table'
    id = Column(Integer, primary_key=True)
    for item in columns:
        locals()[item] = Column(String)
    id_project = Column(Integer, ForeignKey('project.id_project'))
    id_app = Column(Integer, ForeignKey('app.id_app'))
    value = Column(String)
    note_1 = Column(String)
    note_2 = Column(String)

def update_new(project_name, market, power_train, develop_case, df):
    engine = create_engine("mysql+mysqlconnector://test_user_1:Sql123456@10.192.85.133/db_21xe_clone")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    df.replace({np.nan: ''}, inplace=True)

    existing_project = (session.query(Project).filter_by(project_name=project_name, power_train=power_train, market=market,
               develop_case=develop_case).first())
    print("existing_project: ",existing_project)
    if existing_project is not None:
        project_id = existing_project.id_project
        session.query(MainTable).filter(MainTable.id_project == project_id).delete()
        session.query(App).filter(App.project_id == project_id).delete()
        session.query(Project).filter(Project.id_project == project_id).delete()
        session.query(Header).filter(Header.id_project == project_id).delete()
        session.commit()
    project = Project(project_name=project_name, power_train=power_train, market=market,
                      develop_case=develop_case)
    session.add(project)
    session.commit()

    project_id = (session.query(Project.id_project).filter_by(project_name=project_name, power_train=power_train, market=market, develop_case=develop_case).first())[0]

    app_list = []
    app_infor_df = df.iloc[:6, 129:]
    app_infor_df_rotated = app_infor_df.T
    app_infor = app_infor_df_rotated.to_records(index=False)
    app_list.extend([tuple(record) for record in app_infor if any(record)])
    app_objects = [
        App(project_id=project_id, market=app[0], engine=app[1], gearbox=app[2], axle=app[3], handle=app[4],
            app=app[5]) for app in app_list]

    session.bulk_save_objects(app_objects)
    session.commit()



    project_id = (session.query(Project.id_project).filter_by(project_name=project_name, power_train=power_train, market=market, develop_case=develop_case).first())[0]

    print("project_id: ", project_id)
    header_infor = df.iloc[:6, 0:129]
    print("header_infor: ", header_infor)
    header_infor = header_infor.to_records(index=False)
    header_infor = header_infor.tolist()
    for item in header_infor:
        item = (project_id,) + item
        print("item: ", item)

        item_dict = {'id_project': item[0], **{f'col{i}': item[i] for i in range(1, len(item))}}
        header_instance = Header(**item_dict)

        session.add(header_instance)
        session.commit()
        print("pass")


    main_table_df = df.iloc[6:, 0:128]
    main_table_list = main_table_df.to_records(index=False)
    characters_to_omit = "<>'\"!#$%^&[]"
    translation_table = str.maketrans("", "", characters_to_omit)
    main_table_list = [
        [s.translate(translation_table) if s is not None else '' for s in sublist]
        for sublist in main_table_list
    ]

    main_table_objects = []

    app_list =  session.query(App.id_app).filter_by(project_id=project_id).all()
    app_list = [item[0] for item in app_list]
    for index_element, element in enumerate(main_table_list):

        for app in app_list:
            config_value = str(df.iloc[6 + index_element, 129 + app_list.index(app)])
            note_1 = str(df.iloc[6 + index_element, 129 + len(app_list)])
            note_2 = str(df.iloc[6 + index_element, 130 + len(app_list)])

            config_value = ''.join(char for char in config_value if char not in characters_to_omit)
            note_1 = ''.join(char for char in note_1 if char not in characters_to_omit)
            note_2 = ''.join(char for char in note_2 if char not in characters_to_omit)

            main_table_objects.append(
                MainTable(action=element[0], cadic_number=element[1], id_project=project_id, id_app=app,
                          value=config_value, note_1=note_1, note_2=note_2, snt = element[2], regulations = element[3], pep = element[4], Other = element[5], good_design = element[6], y0 = element[7], y0_number = element[8], car_recurrence_prevention = element[9], solution = element[10], solution_number = element[11], common_validation_item = element[12], procedure_item = element[13], requirement = element[14], step1_pt_jp = element[15], step2_pt_jp = element[16], step1_vt_jp = element[17], step2_vt_jp = element[18], step3_vt_jp = element[19], lv1_ct_jp = element[20], lv2_ct_jp = element[21], lv3_ct_jp = element[22], lv4_ct_jp = element[23], comment_ct_jp = element[24], step1_pt_en = element[25], step2_pt_en = element[26], step1_vt_en = element[27], step2_vt_en = element[28], step3_vt_en = element[29], lv1_ct_en = element[30], lv2_ct_en = element[31], lv3_ct_en = element[32], lv4_ct_en = element[33], comment_ct_en = element[34], digital_evaluation_app = element[35], pf_evaluation_app = element[36], physical_evaluation_app = element[37], kca_project_group_deploy = element[38], team_deploy = element[39], manager_name_deploy = element[40], id_or_mail_account_deploy = element[41], name_of_person_in_charge_deploy = element[42], id_or_mail_account_2_deploy = element[43], target_value_deploy = element[44], comment_deploy = element[45], kca_project_group_ac = element[46], team_ac = element[47], manager_name_ac = element[48], id_or_mail_account_ac = element[49], name_of_person_in_charge_ac = element[50], id_or_mail_account_2_ac = element[51], agreement_of_target_ac = element[52], comment_ac = element[53], kca_project_group_digital = element[54], team_digital = element[55], manager_name_digital = element[56], id_or_mail_account_digital = element[57], evaluation_responsible_digital = element[58], id_or_mail_account_2_digital = element[59], evaluate_or_not_ds = element[60], result_first_ds = element[61], report_number_ds = element[62], number_of_qbase_ds = element[63], qbase_number_ds = element[64], result_counter_ds = element[65], comment_ds = element[66], evaluate_or_not_dc = element[67], result_first_dc = element[68], report_number_dc = element[69], number_of_qbase_dc = element[70], qbase_number_dc = element[71], result_counter_dc = element[72], comment_dc = element[73], kca_project_group_ppc = element[74], team_ppc = element[75], manager_name_ppc = element[76], id_or_mail_account_ppc = element[77], evaluation_responsible_ppc = element[78], id_or_mail_account_2_ppc = element[79], evaluate_or_not_pfc = element[80], confirmation_first_pfc = element[81], feedback_timing_pfc = element[82], result_first_pfc = element[83], confirmation_completion_pfc = element[84], report_number_pfc = element[85], number_of_qbase_pfc = element[86], qbase_number_pfc = element[87], result_counter_pfc = element[88], confirmation_completion_date_pfc = element[89], comment_pfc = element[90], kca_project_group_ppe = element[91], team_ppe = element[92], manager_name_ppe = element[93], id_or_mail_account_ppe = element[94], evaluation_responsible_ppe = element[95], id_or_mail_account_2_ppe = element[96], evaluate_or_not_vc = element[97], confirm_first_date_vc = element[98], result_first_vc = element[99], confirm_first_completion_vc = element[100], report_number_vc = element[101], number_of_qbase_vc = element[102], qbase_number_vc = element[103], result_counter_vc = element[104], confirm_first_completion_2_vc = element[105], comment_vc = element[106], evaluate_or_not_pt1 = element[107], confirm_first_date_pt1 = element[108], result_first_pt1 = element[109], confirm_first_completion_pt1 = element[110], report_number_pt1 = element[111], number_of_qbase_pt1 = element[112], qbase_number_pt1 = element[113], result_counter_pt1 = element[114], confirm_first_completion_2_pt1 = element[115], comment_pt1 = element[116], evaluate_or_not_pt2 = element[117], confirmation_first_time_pt2 = element[118], result_first_pt2 = element[119], confirm_first_completion_pt2 = element[120], report_number_pt2 = element[121], number_of_qbase_pt2 = element[122], qbase_number_pt2 = element[123], result_counter_pt2 = element[124], confirm_first_completion_2_pt2 = element[125], comment_pt2 = element[126], common_unique = element[127]))

        if index_element % 500 == 0 and index_element > 0:
            session.bulk_save_objects(main_table_objects)
            session.commit()
            main_table_objects = []

    if main_table_objects:
        session.bulk_save_objects(main_table_objects)
        session.commit()

    session.close()
    print("done")
project_name = "ffff"
market = "US"
power_train = "EV"
develop_case = "CASE1.5"
df = pd.read_csv(r"C:\Users\KNT20162\Downloads\2024-02-27T08-40_export.csv", header=None)
update_new(project_name, market, power_train, develop_case, df)