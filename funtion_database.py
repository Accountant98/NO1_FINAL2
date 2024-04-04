import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String,DateTime, ForeignKey, update, func,and_, MetaData
from hashlib import sha256
from sqlalchemy.orm import sessionmaker, aliased, declarative_base,class_mapper
import streamlit as st
import numpy as np
import decouple
import os

# from create_cadics import create_cadics
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

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    permission = Column(String)
    project = Column(String)

def connect_db():
    database_url = decouple.config('DATABASE_URL')
    database_username = decouple.config('DATABASE_USERNAME')
    database_password = decouple.config('DATABASE_PASSWORD')
    database_name = decouple.config('DATABASE_NAME')
    str_connect="mysql+mysqlconnector://"+database_username+":"+ database_password+"@"+database_url +"/"+database_name
    engine=create_engine(str_connect)
    return engine
# def query_data(project_name, market, powertrain, develop_case, group, lot):
#     #engine =create_engine("mysql+mysqlconnector://test_user_1:Sql123456@10.192.85.133/db_21xe_clone")
#     engine=connect_db()
#     Base.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     project = session.query(Project).filter_by(project_name=project_name, power_train=powertrain, market=market, develop_case=develop_case).first()

#     if project is not None:
#         id_project = project.id_project
#         sum_config = session.query(func.count(App.app)).filter_by(project_id=id_project).first()[0]
#         min_id = session.query(func.min(MainTable.id)).filter(MainTable.id_project == id_project).scalar()
#         #print("min_id: ", min_id)

#         header_query = session.query(Header).filter_by(id_project=id_project).all()
#         header_data = [row.__dict__ for row in header_query]
#         header_df = pd.DataFrame.from_records(header_data)
#         column_order = [column.name for column in Header.__table__.columns]
#         header_df = header_df[column_order]
#         header_df.drop(['id', 'id_project'], axis=1, inplace=True)
#         # print("header_df: ", header_df)
#         app_query = session.query(App.market, App.engine, App.gearbox, App.axle, App.handle, App.app).filter_by(project_id = id_project).all()

#         app_df = pd.DataFrame(app_query)
#         app_df.fillna('')
#         app_df_transposed = app_df.transpose()
#         app_df_transposed.reset_index(drop=True, inplace=True)

#         result_df = pd.concat([header_df, app_df_transposed], axis=1)
#         result_df.insert(result_df.shape[1], 'Note_1', '')
#         result_df.insert(result_df.shape[1], 'Note_2', '')

#         main_table_alias = aliased(MainTable)
#         columns_to_query = [
#             getattr(MainTable, column_name).label(column_name)
#             for column_name in columns
#         ]
#         substring_columns = [
#             func.SUBSTRING_INDEX(
#                 func.SUBSTRING_INDEX(
#                     func.GROUP_CONCAT(main_table_alias.value.op('ORDER BY')(main_table_alias.id_app)),
#                     ',', counter + 1),
#                 ',', -1
#             )
#             for counter in range(0, sum_config)
#         ]
#         query_data = (
#             session.query(*columns_to_query, *substring_columns, MainTable.note_1, MainTable.note_2)
#             .join(main_table_alias,
#                   MainTable.id == main_table_alias.id)
#             .filter(MainTable.id_project == id_project)
#         )
#         if lot == "DS" or lot == "DC":
#             query_data = query_data.filter(MainTable.kca_project_group_digital == group)
#         elif lot == "PFC":
#             query_data = query_data.filter(MainTable.kca_project_group_ppc == group)
#         elif lot == "VC" or lot == "PT1" or lot == "PT2":
#             query_data = query_data.filter(MainTable.kca_project_group_ppe == group)
#         if lot != "ALL":
#             lot_lower = lot.lower()
#             query_data = query_data.filter(getattr(MainTable, f'evaluate_or_not_{lot_lower}') == 'YES')
#         query_data = query_data.group_by(func.FLOOR((MainTable.id - min_id) / sum_config))

#         data_df = pd.read_sql(query_data.statement, session.bind)
#         data_df.insert(data_df.columns.get_loc('common_unique') + 1, 'empty_column', '')
#         data_df.fillna('', inplace=True)
#         data_df.set_index(pd.RangeIndex(start=6, stop=6 + len(data_df)), inplace=True)
#         data_df.columns = result_df.columns
#         result_df_matched = pd.concat([result_df, data_df], axis=0)
#         result_df_matched.columns = range(1, len(result_df_matched.columns) + 1)
#         # print("result_df_matched: ", result_df_matched)
#         app_alias = aliased(App)
#         id_app_list = (
#             session.query(app_alias.id_app)
#             .filter(app_alias.project_id == id_project)
#             .all()
#         )
#         id_app_list = [row[0] for row in id_app_list]

#         if header_df is not None:
#             session.close()
#             return  session, result_df_matched, id_project, id_app_list
#     else:
#         st.error("Project not found in the database.")
#         return None,frame_empty(),None,None
#     session.close()

def update_edit(data_edit, session, result_df_matched, id_project, id_app_list):
    try:
        characters_to_omit = "<>'\"!#$%^&[]"
        translation_table = str.maketrans("", "", characters_to_omit)
        header_df_after_list = data_edit.iloc[:6, 0:129].values.tolist()
        header_df_before_list = result_df_matched.iloc[:6, 0:129].values.tolist()
        set_header_before = set(map(tuple, header_df_before_list))
        set_header_after = set(map(tuple, header_df_after_list))
        header_different_set = set_header_after - set_header_before
        header_different_list = list(map(list, header_different_set))
        #print("header_different_list: ",header_different_list)
        if header_different_list!=[]:
            header_df_after_list = [
                [s.translate(translation_table) if s is not None else '' for s in sublist]
                for sublist in header_df_after_list
            ]
            session.query(Header).filter(Header.id_project == id_project).delete()
            for item in header_df_after_list:
                item = (id_project,) + tuple(item)
                item_dict = {'id_project': item[0], **{f'col{i}': item[i] for i in range(1, len(item))}}
                header_instance = Header(**item_dict)

                session.add(header_instance)
                session.commit()
        else:
            None
            #print("Header not edited")
        data_edit_list = data_edit.iloc[6:].values.tolist()
        result_df_list = result_df_matched.iloc[6:].values.tolist()

        set_data_edit = set(map(tuple, data_edit_list))
        set_result_df = set(map(tuple, result_df_list))
        different_set = set_data_edit - set_result_df
        different_list = list(map(list, different_set))

        different_list = [
            [s.translate(translation_table) if s is not None else '' for s in sublist]
            for sublist in different_list
        ]
        for sublist in different_list:
            for i, value in enumerate(sublist):
                if value is None:
                    sublist[i] = ''
        different_tuple_list = [tuple(row) for row in different_list]

        columns = ['action', 'snt', 'regulations', 'pep', 'Other', 'good_design', 'y0', 'y0_number','car_recurrence_prevention', 'solution', 'solution_number', 'common_validation_item','procedure_item', 'requirement', 'step1_pt_jp', 'step2_pt_jp', 'step1_vt_jp', 'step2_vt_jp','step3_vt_jp', 'lv1_ct_jp', 'lv2_ct_jp', 'lv3_ct_jp', 'lv4_ct_jp', 'comment_ct_jp','step1_pt_en', 'step2_pt_en', 'step1_vt_en', 'step2_vt_en', 'step3_vt_en', 'lv1_ct_en','lv2_ct_en', 'lv3_ct_en', 'lv4_ct_en', 'comment_ct_en', 'digital_evaluation_app','pf_evaluation_app', 'physical_evaluation_app', 'kca_project_group_deploy', 'team_deploy','manager_name_deploy', 'id_or_mail_account_deploy', 'name_of_person_in_charge_deploy','id_or_mail_account_2_deploy', 'target_value_deploy', 'comment_deploy', 'kca_project_group_ac','team_ac', 'manager_name_ac', 'id_or_mail_account_ac', 'name_of_person_in_charge_ac','id_or_mail_account_2_ac', 'agreement_of_target_ac', 'comment_ac', 'kca_project_group_digital','team_digital', 'manager_name_digital', 'id_or_mail_account_digital','evaluation_responsible_digital', 'id_or_mail_account_2_digital', 'evaluate_or_not_ds','result_first_ds', 'report_number_ds', 'number_of_qbase_ds', 'qbase_number_ds','result_counter_ds', 'comment_ds', 'evaluate_or_not_dc', 'result_first_dc', 'report_number_dc','number_of_qbase_dc', 'qbase_number_dc', 'result_counter_dc', 'comment_dc','kca_project_group_ppc', 'team_ppc', 'manager_name_ppc', 'id_or_mail_account_ppc','evaluation_responsible_ppc', 'id_or_mail_account_2_ppc', 'evaluate_or_not_pfc','confirmation_first_pfc', 'feedback_timing_pfc', 'result_first_pfc','confirmation_completion_pfc', 'report_number_pfc', 'number_of_qbase_pfc', 'qbase_number_pfc','result_counter_pfc', 'confirmation_completion_date_pfc', 'comment_pfc', 'kca_project_group_ppe','team_ppe', 'manager_name_ppe', 'id_or_mail_account_ppe', 'evaluation_responsible_ppe','id_or_mail_account_2_ppe', 'evaluate_or_not_vc', 'confirm_first_date_vc', 'result_first_vc','confirm_first_completion_vc', 'report_number_vc', 'number_of_qbase_vc', 'qbase_number_vc','result_counter_vc', 'confirm_first_completion_2_vc', 'comment_vc', 'evaluate_or_not_pt1','confirm_first_date_pt1', 'result_first_pt1', 'confirm_first_completion_pt1','report_number_pt1', 'number_of_qbase_pt1', 'qbase_number_pt1', 'result_counter_pt1','confirm_first_completion_2_pt1', 'comment_pt1', 'evaluate_or_not_pt2','confirmation_first_time_pt2', 'result_first_pt2', 'confirm_first_completion_pt2','report_number_pt2', 'number_of_qbase_pt2', 'qbase_number_pt2', 'result_counter_pt2','confirm_first_completion_2_pt2', 'comment_pt2', 'common_unique', 'value', 'note_1', 'note_2']
        result_list = []
        for t in different_tuple_list:
            key = t[1]
            new_tuple = t[0:1] + t[2:128] + t[129:]
            result_list.append((key, new_tuple))
        result = []
        for item in result_list:
            main_tuple = item[1]
            end_index = len(main_tuple) - 1
            prefix = main_tuple[:127]
            suffix = main_tuple[127:(end_index - 1)]
            for value in suffix:
                new_tuple = prefix + (value,) + (main_tuple[end_index], main_tuple[end_index - 1])
                result.append((item[0], new_tuple))

        counter_app = 0
        for idx, item in enumerate(result):
            cadic_number = item[0]
            values = item[1] + (cadic_number,)

            update_stmt = (
                update(MainTable)
                .where((MainTable.id_project == id_project) & (MainTable.id_app == id_app_list[counter_app]) & (MainTable.cadic_number == cadic_number))
                .values(dict(zip(columns, values)))
            )
            counter_app += 1
            if counter_app > len(id_app_list) - 1:
                counter_app = 0
            session.execute(update_stmt)
        session.commit()
        chars_to_replace = ['<', '>', "'", '"', '!', '#', '$', '%', '^', '&', '[', ']']
        for col in data_edit.columns:
            for char in chars_to_replace:
                data_edit[col] = data_edit[col].str.replace(char, '')
        return data_edit

    except Exception as e:
        st.error(f"Error saving changes: {e}")
        #print("Error converting to DataFrame or saving changes.")
    finally:
        session.close()

# def update_new(project_name, market, power_train, develop_case, df):
#     #engine = create_engine("mysql+mysqlconnector://test_user_1:Sql123456@10.192.85.133/db_21xe_clone")
#     engine=connect_db()
#     Base.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     df.replace({np.nan: ''}, inplace=True)

#     existing_project = (session.query(Project).filter_by(project_name=project_name, power_train=power_train, market=market,
#                develop_case=develop_case).first())
#     #print("existing_project: ",existing_project)
#     if existing_project is not None:
#         project_id = existing_project.id_project
#         session.query(MainTable).filter(MainTable.id_project == project_id).delete()
#         session.query(App).filter(App.project_id == project_id).delete()
#         session.query(Project).filter(Project.id_project == project_id).delete()
#         session.query(Header).filter(Header.id_project == project_id).delete()
#         session.commit()
#     project = Project(project_name=project_name, power_train=power_train, market=market,
#                       develop_case=develop_case)
#     session.add(project)
#     session.commit()

#     project_id = (session.query(Project.id_project).filter_by(project_name=project_name, power_train=power_train, market=market, develop_case=develop_case).first())[0]

#     app_list = []
#     app_infor_df = df.iloc[:6, 129:]
#     app_infor_df_rotated = app_infor_df.T
#     app_infor = app_infor_df_rotated.to_records(index=False)
#     app_list.extend([tuple(record) for record in app_infor if any(record)])
#     app_objects = [
#         App(project_id=project_id, market=app[0], engine=app[1], gearbox=app[2], axle=app[3], handle=app[4],
#             app=app[5]) for app in app_list]

#     session.bulk_save_objects(app_objects)
#     session.commit()



#     project_id = (session.query(Project.id_project).filter_by(project_name=project_name, power_train=power_train, market=market, develop_case=develop_case).first())[0]

#     #print("project_id: ", project_id)
#     header_infor = df.iloc[:6, 0:129]
#     #print("header_infor: ", header_infor)
#     header_infor = header_infor.to_records(index=False)
#     header_infor = header_infor.tolist()
#     for item in header_infor:
#         item = (project_id,) + item
#         #print("item: ", item)
#         item_dict = {'id_project': item[0], **{f'col{i}': item[i] for i in range(1, len(item))}}
#         header_instance = Header(**item_dict)

#         session.add(header_instance)
#         session.commit()
#         #print("pass")


#     main_table_df = df.iloc[6:, 0:128]
#     main_table_list = main_table_df.to_records(index=False)
#     characters_to_omit = "<>'\"!#$%^&[]"
#     translation_table = str.maketrans("", "", characters_to_omit)
#     main_table_list = [
#         [s.translate(translation_table) if s is not None else '' for s in sublist]
#         for sublist in main_table_list
#     ]

#     main_table_objects = []

#     app_list =  session.query(App.id_app).filter_by(project_id=project_id).all()
#     app_list = [item[0] for item in app_list]
#     for index_element, element in enumerate(main_table_list):

#         for app in app_list:
#             config_value = str(df.iloc[6 + index_element, 129 + app_list.index(app)])
#             note_1 = str(df.iloc[6 + index_element, 129 + len(app_list)])
#             note_2 = str(df.iloc[6 + index_element, 130 + len(app_list)])

#             config_value = ''.join(char for char in config_value if char not in characters_to_omit)
#             note_1 = ''.join(char for char in note_1 if char not in characters_to_omit)
#             note_2 = ''.join(char for char in note_2 if char not in characters_to_omit)

#             main_table_objects.append(
#                 MainTable(action=element[0], cadic_number=element[1], id_project=project_id, id_app=app,
#                           value=config_value, note_1=note_1, note_2=note_2, snt = element[2], regulations = element[3], pep = element[4], Other = element[5], good_design = element[6], y0 = element[7], y0_number = element[8], car_recurrence_prevention = element[9], solution = element[10], solution_number = element[11], common_validation_item = element[12], procedure_item = element[13], requirement = element[14], step1_pt_jp = element[15], step2_pt_jp = element[16], step1_vt_jp = element[17], step2_vt_jp = element[18], step3_vt_jp = element[19], lv1_ct_jp = element[20], lv2_ct_jp = element[21], lv3_ct_jp = element[22], lv4_ct_jp = element[23], comment_ct_jp = element[24], step1_pt_en = element[25], step2_pt_en = element[26], step1_vt_en = element[27], step2_vt_en = element[28], step3_vt_en = element[29], lv1_ct_en = element[30], lv2_ct_en = element[31], lv3_ct_en = element[32], lv4_ct_en = element[33], comment_ct_en = element[34], digital_evaluation_app = element[35], pf_evaluation_app = element[36], physical_evaluation_app = element[37], kca_project_group_deploy = element[38], team_deploy = element[39], manager_name_deploy = element[40], id_or_mail_account_deploy = element[41], name_of_person_in_charge_deploy = element[42], id_or_mail_account_2_deploy = element[43], target_value_deploy = element[44], comment_deploy = element[45], kca_project_group_ac = element[46], team_ac = element[47], manager_name_ac = element[48], id_or_mail_account_ac = element[49], name_of_person_in_charge_ac = element[50], id_or_mail_account_2_ac = element[51], agreement_of_target_ac = element[52], comment_ac = element[53], kca_project_group_digital = element[54], team_digital = element[55], manager_name_digital = element[56], id_or_mail_account_digital = element[57], evaluation_responsible_digital = element[58], id_or_mail_account_2_digital = element[59], evaluate_or_not_ds = element[60], result_first_ds = element[61], report_number_ds = element[62], number_of_qbase_ds = element[63], qbase_number_ds = element[64], result_counter_ds = element[65], comment_ds = element[66], evaluate_or_not_dc = element[67], result_first_dc = element[68], report_number_dc = element[69], number_of_qbase_dc = element[70], qbase_number_dc = element[71], result_counter_dc = element[72], comment_dc = element[73], kca_project_group_ppc = element[74], team_ppc = element[75], manager_name_ppc = element[76], id_or_mail_account_ppc = element[77], evaluation_responsible_ppc = element[78], id_or_mail_account_2_ppc = element[79], evaluate_or_not_pfc = element[80], confirmation_first_pfc = element[81], feedback_timing_pfc = element[82], result_first_pfc = element[83], confirmation_completion_pfc = element[84], report_number_pfc = element[85], number_of_qbase_pfc = element[86], qbase_number_pfc = element[87], result_counter_pfc = element[88], confirmation_completion_date_pfc = element[89], comment_pfc = element[90], kca_project_group_ppe = element[91], team_ppe = element[92], manager_name_ppe = element[93], id_or_mail_account_ppe = element[94], evaluation_responsible_ppe = element[95], id_or_mail_account_2_ppe = element[96], evaluate_or_not_vc = element[97], confirm_first_date_vc = element[98], result_first_vc = element[99], confirm_first_completion_vc = element[100], report_number_vc = element[101], number_of_qbase_vc = element[102], qbase_number_vc = element[103], result_counter_vc = element[104], confirm_first_completion_2_vc = element[105], comment_vc = element[106], evaluate_or_not_pt1 = element[107], confirm_first_date_pt1 = element[108], result_first_pt1 = element[109], confirm_first_completion_pt1 = element[110], report_number_pt1 = element[111], number_of_qbase_pt1 = element[112], qbase_number_pt1 = element[113], result_counter_pt1 = element[114], confirm_first_completion_2_pt1 = element[115], comment_pt1 = element[116], evaluate_or_not_pt2 = element[117], confirmation_first_time_pt2 = element[118], result_first_pt2 = element[119], confirm_first_completion_pt2 = element[120], report_number_pt2 = element[121], number_of_qbase_pt2 = element[122], qbase_number_pt2 = element[123], result_counter_pt2 = element[124], confirm_first_completion_2_pt2 = element[125], comment_pt2 = element[126], common_unique = element[127]))

#         if index_element % 500 == 0 and index_element > 0:
#             session.bulk_save_objects(main_table_objects)
#             session.commit()
#             main_table_objects = []

#     if main_table_objects:
#         session.bulk_save_objects(main_table_objects)
#         session.commit()

#     session.close()
#     df = df.applymap(lambda x: replace_symbol(x) if isinstance(x, str) else x)
#     return  session, df, project_id, app_list


def update_new(project_name, market, power_train, develop_case, df, group):
    #engine = create_engine("mysql+mysqlconnector://test_user_1:Sql123456@10.192.85.133/db_21xe_clone")
    engine=connect_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    df.replace({np.nan: ''}, inplace=True)
    df['preventive_1'] = ''
    df['preventive_2'] = ''
    #print("len: ",df.shape[1])
    existing_project = (session.query(Project).filter_by(project_name=project_name, power_train=power_train, market=market,
               develop_case=develop_case).first())
    #print("existing_project: ",existing_project)
    if existing_project is not None:
        project_id = existing_project.id_project
        session.query(App).filter(App.project_id == project_id).all()
        session.query(Header).filter(Header.id_project == project_id).all()
    else:
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

        header_infor = df.iloc[:6, 0:129]
        #print("header_infor: ", header_infor)
        header_infor = header_infor.to_records(index=False)
        header_infor = header_infor.tolist()
        for item in header_infor:
            item = (project_id,) + item
            #print("item: ", item)

            item_dict = {'id_project': item[0], **{f'col{i}': item[i] for i in range(1, len(item))}}
            header_instance = Header(**item_dict)

            session.add(header_instance)
            session.commit()
            #print("pass")


    main_table_df = df.iloc[6:, 0:128]
    main_table_list = main_table_df.to_records(index=False)
    characters_to_omit = "<>'\"!#$%^&[]"
    translation_table = str.maketrans("", "", characters_to_omit)
    main_table_list = [
        [s.translate(translation_table) if s is not None else '' for s in sublist]
        for sublist in main_table_list
    ]
    main_table_cadic_number_list = main_table_df.iloc[6:, 1].tolist()
    main_table_cadic_number_tuple = tuple(main_table_cadic_number_list)
    #print(main_table_cadic_number_tuple)

    session.query(MainTable).filter(
        (MainTable.id_project == project_id) &
        (((MainTable.kca_project_group_digital.in_(group)) |
     (MainTable.kca_project_group_ppc.in_(group)) |
     (MainTable.kca_project_group_ppe.in_(group))))
    ).delete()

    session.commit()

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
    df = df.applymap(lambda x: replace_symbol(x) if isinstance(x, str) else x)
    return  session, df, project_id, app_list
    




def log_in(username, password):
    password=sha256(password.encode('utf-8')).hexdigest()
    #engine = create_engine("mysql+mysqlconnector://test_user_1:Sql123456@10.192.85.133/db_21xe_clone")
    engine=connect_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(User.username, User.permission, User.project).filter_by(username=username, password = password).first()
    if result is not None:
        session.close()
    else:
        session.close()
        result = (username, None,None)
    return result


def offline_edit(project_name, market, power_train, develop_case, df_new, df_old):
    engine = connect_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    mapper = class_mapper(MainTable)
    columns = [col for col in list(mapper.columns) if col.key != 'id']

    df_new.replace({np.nan: ''}, inplace=True)

    project_id = (session.query(Project.id_project).filter_by(project_name=project_name, power_train=power_train, market=market, develop_case=develop_case).first()).id_project
    main_table_df = df_new.iloc[6:, 0:128]
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
    #==========================add column Note1, Note2===========================================
    # if len(df_new.columns)==129 + len(app_list):
    #     df_new[129 + len(app_list)]=None
    #     df_new[130 + len(app_list)]=None
    num_col=len(df_new.columns)
    i=0
    min_col=130 + len(app_list)
    while len(df_new.columns)<=min_col:
        df_new[num_col+i]=None
        i=i+1

    for index_element, element in enumerate(main_table_list):

        for app in app_list:
            config_value = str(df_new.iloc[6 + index_element, 129 + app_list.index(app)])
            note_1 = str(df_new.iloc[6 + index_element, 129 + len(app_list)])
            note_2 = str(df_new.iloc[6 + index_element, 130 + len(app_list)])
            config_value = ''.join(char for char in config_value if char not in characters_to_omit)
            note_1 = ''.join(char for char in note_1 if char not in characters_to_omit)
            note_2 = ''.join(char for char in note_2 if char not in characters_to_omit)

            main_table_objects.append(
                MainTable(action=element[0], cadic_number=element[1], snt = element[2], regulations = element[3], pep = element[4], Other = element[5], good_design = element[6], y0 = element[7], y0_number = element[8], car_recurrence_prevention = element[9], solution = element[10], solution_number = element[11], common_validation_item = element[12], procedure_item = element[13], requirement = element[14], step1_pt_jp = element[15], step2_pt_jp = element[16], step1_vt_jp = element[17], step2_vt_jp = element[18], step3_vt_jp = element[19], lv1_ct_jp = element[20], lv2_ct_jp = element[21], lv3_ct_jp = element[22], lv4_ct_jp = element[23], comment_ct_jp = element[24], step1_pt_en = element[25], step2_pt_en = element[26], step1_vt_en = element[27], step2_vt_en = element[28], step3_vt_en = element[29], lv1_ct_en = element[30], lv2_ct_en = element[31], lv3_ct_en = element[32], lv4_ct_en = element[33], comment_ct_en = element[34], digital_evaluation_app = element[35], pf_evaluation_app = element[36], physical_evaluation_app = element[37], kca_project_group_deploy = element[38], team_deploy = element[39], manager_name_deploy = element[40], id_or_mail_account_deploy = element[41], name_of_person_in_charge_deploy = element[42], id_or_mail_account_2_deploy = element[43], target_value_deploy = element[44], comment_deploy = element[45], kca_project_group_ac = element[46], team_ac = element[47], manager_name_ac = element[48], id_or_mail_account_ac = element[49], name_of_person_in_charge_ac = element[50], id_or_mail_account_2_ac = element[51], agreement_of_target_ac = element[52], comment_ac = element[53], kca_project_group_digital = element[54], team_digital = element[55], manager_name_digital = element[56], id_or_mail_account_digital = element[57], evaluation_responsible_digital = element[58], id_or_mail_account_2_digital = element[59], evaluate_or_not_ds = element[60], result_first_ds = element[61], report_number_ds = element[62], number_of_qbase_ds = element[63], qbase_number_ds = element[64], result_counter_ds = element[65], comment_ds = element[66], evaluate_or_not_dc = element[67], result_first_dc = element[68], report_number_dc = element[69], number_of_qbase_dc = element[70], qbase_number_dc = element[71], result_counter_dc = element[72], comment_dc = element[73], kca_project_group_ppc = element[74], team_ppc = element[75], manager_name_ppc = element[76], id_or_mail_account_ppc = element[77], evaluation_responsible_ppc = element[78], id_or_mail_account_2_ppc = element[79], evaluate_or_not_pfc = element[80], confirmation_first_pfc = element[81], feedback_timing_pfc = element[82], result_first_pfc = element[83], confirmation_completion_pfc = element[84], report_number_pfc = element[85], number_of_qbase_pfc = element[86], qbase_number_pfc = element[87], result_counter_pfc = element[88], confirmation_completion_date_pfc = element[89], comment_pfc = element[90], kca_project_group_ppe = element[91], team_ppe = element[92], manager_name_ppe = element[93], id_or_mail_account_ppe = element[94], evaluation_responsible_ppe = element[95], id_or_mail_account_2_ppe = element[96], evaluate_or_not_vc = element[97], confirm_first_date_vc = element[98], result_first_vc = element[99], confirm_first_completion_vc = element[100], report_number_vc = element[101], number_of_qbase_vc = element[102], qbase_number_vc = element[103], result_counter_vc = element[104], confirm_first_completion_2_vc = element[105], comment_vc = element[106], evaluate_or_not_pt1 = element[107], confirm_first_date_pt1 = element[108], result_first_pt1 = element[109], confirm_first_completion_pt1 = element[110], report_number_pt1 = element[111], number_of_qbase_pt1 = element[112], qbase_number_pt1 = element[113], result_counter_pt1 = element[114], confirm_first_completion_2_pt1 = element[115], comment_pt1 = element[116], evaluate_or_not_pt2 = element[117], confirmation_first_time_pt2 = element[118], result_first_pt2 = element[119], confirm_first_completion_pt2 = element[120], report_number_pt2 = element[121], number_of_qbase_pt2 = element[122], qbase_number_pt2 = element[123], result_counter_pt2 = element[124], confirm_first_completion_2_pt2 = element[125], comment_pt2 = element[126], common_unique = element[127], id_project=project_id, id_app=app,
                          value=config_value, note_1=note_1, note_2=note_2))

    new_for_compare = [tuple(obj.__dict__.values()) for obj in main_table_objects]
    new_for_compare = [tuple[1:] for tuple in new_for_compare]

    df_old.replace({np.nan: ''}, inplace=True)

    main_table_df = df_old.iloc[6:, 0:128]
    main_table_list = main_table_df.to_records(index=False)

    main_table_objects = []
    for index_element, element in enumerate(main_table_list):
        for app in app_list:
            config_value = str(df_old.iloc[6 + index_element, 129 + app_list.index(app)])
            note_1 = str(df_old.iloc[6 + index_element, 129 + len(app_list)])
            note_2 = str(df_old.iloc[6 + index_element, 130 + len(app_list)])
            config_value = ''.join(char for char in config_value if char not in characters_to_omit)
            note_1 = ''.join(char for char in note_1 if char not in characters_to_omit)
            note_2 = ''.join(char for char in note_2 if char not in characters_to_omit)

            main_table_objects.append(
                MainTable(action=element[0], cadic_number=element[1], snt = element[2], regulations = element[3], pep = element[4], Other = element[5], good_design = element[6], y0 = element[7], y0_number = element[8], car_recurrence_prevention = element[9], solution = element[10], solution_number = element[11], common_validation_item = element[12], procedure_item = element[13], requirement = element[14], step1_pt_jp = element[15], step2_pt_jp = element[16], step1_vt_jp = element[17], step2_vt_jp = element[18], step3_vt_jp = element[19], lv1_ct_jp = element[20], lv2_ct_jp = element[21], lv3_ct_jp = element[22], lv4_ct_jp = element[23], comment_ct_jp = element[24], step1_pt_en = element[25], step2_pt_en = element[26], step1_vt_en = element[27], step2_vt_en = element[28], step3_vt_en = element[29], lv1_ct_en = element[30], lv2_ct_en = element[31], lv3_ct_en = element[32], lv4_ct_en = element[33], comment_ct_en = element[34], digital_evaluation_app = element[35], pf_evaluation_app = element[36], physical_evaluation_app = element[37], kca_project_group_deploy = element[38], team_deploy = element[39], manager_name_deploy = element[40], id_or_mail_account_deploy = element[41], name_of_person_in_charge_deploy = element[42], id_or_mail_account_2_deploy = element[43], target_value_deploy = element[44], comment_deploy = element[45], kca_project_group_ac = element[46], team_ac = element[47], manager_name_ac = element[48], id_or_mail_account_ac = element[49], name_of_person_in_charge_ac = element[50], id_or_mail_account_2_ac = element[51], agreement_of_target_ac = element[52], comment_ac = element[53], kca_project_group_digital = element[54], team_digital = element[55], manager_name_digital = element[56], id_or_mail_account_digital = element[57], evaluation_responsible_digital = element[58], id_or_mail_account_2_digital = element[59], evaluate_or_not_ds = element[60], result_first_ds = element[61], report_number_ds = element[62], number_of_qbase_ds = element[63], qbase_number_ds = element[64], result_counter_ds = element[65], comment_ds = element[66], evaluate_or_not_dc = element[67], result_first_dc = element[68], report_number_dc = element[69], number_of_qbase_dc = element[70], qbase_number_dc = element[71], result_counter_dc = element[72], comment_dc = element[73], kca_project_group_ppc = element[74], team_ppc = element[75], manager_name_ppc = element[76], id_or_mail_account_ppc = element[77], evaluation_responsible_ppc = element[78], id_or_mail_account_2_ppc = element[79], evaluate_or_not_pfc = element[80], confirmation_first_pfc = element[81], feedback_timing_pfc = element[82], result_first_pfc = element[83], confirmation_completion_pfc = element[84], report_number_pfc = element[85], number_of_qbase_pfc = element[86], qbase_number_pfc = element[87], result_counter_pfc = element[88], confirmation_completion_date_pfc = element[89], comment_pfc = element[90], kca_project_group_ppe = element[91], team_ppe = element[92], manager_name_ppe = element[93], id_or_mail_account_ppe = element[94], evaluation_responsible_ppe = element[95], id_or_mail_account_2_ppe = element[96], evaluate_or_not_vc = element[97], confirm_first_date_vc = element[98], result_first_vc = element[99], confirm_first_completion_vc = element[100], report_number_vc = element[101], number_of_qbase_vc = element[102], qbase_number_vc = element[103], result_counter_vc = element[104], confirm_first_completion_2_vc = element[105], comment_vc = element[106], evaluate_or_not_pt1 = element[107], confirm_first_date_pt1 = element[108], result_first_pt1 = element[109], confirm_first_completion_pt1 = element[110], report_number_pt1 = element[111], number_of_qbase_pt1 = element[112], qbase_number_pt1 = element[113], result_counter_pt1 = element[114], confirm_first_completion_2_pt1 = element[115], comment_pt1 = element[116], evaluate_or_not_pt2 = element[117], confirmation_first_time_pt2 = element[118], result_first_pt2 = element[119], confirm_first_completion_pt2 = element[120], report_number_pt2 = element[121], number_of_qbase_pt2 = element[122], qbase_number_pt2 = element[123], result_counter_pt2 = element[124], confirm_first_completion_2_pt2 = element[125], comment_pt2 = element[126], common_unique = element[127], id_project=project_id, id_app=app,
                          value=config_value, note_1=note_1, note_2=note_2))



    old_for_compare = [tuple(obj.__dict__.values()) for obj in main_table_objects]
    old_for_compare = [tuple[1:] for tuple in old_for_compare]

    list_cadic_number_old = [sub_tuple[1] for sub_tuple in old_for_compare]
    list_cadic_number_new = [sub_tuple[1] for sub_tuple in new_for_compare]
    seen_values = set()
    list_cadic_number_old = [value for value in list_cadic_number_old if (value not in seen_values) and not seen_values.add(value)]
    seen_values = set()
    list_cadic_number_new = [value for value in list_cadic_number_new if (value not in seen_values) and not seen_values.add(value)]



    # Delete cadic case (new khong co, old co)
    delete_cadic_number_list = list(set(list_cadic_number_old) - set(list_cadic_number_new))
    delete_cadic_tuple = []
    if delete_cadic_number_list:
        delete_cadic_number_tuple = tuple(delete_cadic_number_list)
        for cadic_number in delete_cadic_number_list:
            for item in old_for_compare:
                if cadic_number == item[1]:
                    delete_cadic_tuple.append(item)
        session.query(MainTable).filter(
            and_(MainTable.id_project == project_id, MainTable.cadic_number.in_(delete_cadic_number_tuple))).delete()
        session.commit()
    # Add cadic case (new co, old khong co)
    insert_cadic_number_list = list(set(list_cadic_number_new) - set(list_cadic_number_old))
    insert_cadic_tuple = []
    if insert_cadic_number_list:
        main_table_objects = []
        for cadic_number in insert_cadic_number_list:
            for item in new_for_compare:
                if cadic_number == item[1]:
                    insert_cadic_tuple.append(item)

        for sub_element in insert_cadic_tuple:
            main_table_objects.append(MainTable(**{col.key: value for col, value in zip(columns, sub_element)}))

        session.bulk_save_objects(main_table_objects)
        session.commit()

    # Modified cadic case (ca hai co nhung khac nhau)
    new_for_compare_omit_insert_cadic = list(set(new_for_compare) - set(insert_cadic_tuple))
    old_for_compare_omit_delete_cadic = list(set(old_for_compare) - set(delete_cadic_tuple))
    modified_cadic_list = list(set(new_for_compare_omit_insert_cadic) - set(old_for_compare_omit_delete_cadic))
    modified_main_table_objects = []
    if modified_cadic_list:
        for sub_element in modified_cadic_list:
            cadic_updated = sub_element[1]
            id_project_update = sub_element[128]
            app_updated = sub_element[129]

            update_data = {col.key: value for col, value in zip(columns, sub_element)}

            modified_main_table_objects.append(MainTable(**update_data))
            session.query(MainTable).filter(
                (MainTable.id_project == id_project_update) &
                (MainTable.id_app == app_updated) &
                (MainTable.cadic_number == cadic_updated)
            ).update(update_data)
            session.commit()

    header_df_new_list = df_new.iloc[:6, 0:129].values.tolist()
    header_df_old_list = df_old.iloc[:6, 0:129].values.tolist()
    set_header_old = set(map(tuple, header_df_old_list))
    set_header_new = set(map(tuple, header_df_new_list))
    header_different_set = set_header_new - set_header_old
    header_different_list = list(map(list, header_different_set))
    #print("header_different_list: ", header_different_list)
    if header_different_list != []:
        header_df_new_list = [
            [s.translate(translation_table) if s is not None else '' for s in sublist]
            for sublist in header_df_new_list
        ]
        session.query(Header).filter(Header.id_project == project_id).delete()
        for item in header_df_new_list:
            item = (project_id,) + tuple(item)
            item_dict = {'id_project': item[0], **{f'col{i}': item[i] for i in range(1, len(item))}}
            header_instance = Header(**item_dict)

            session.add(header_instance)
            session.commit()

    session.close()


def replace_symbol(input_text):
    if isinstance(input_text,str):
        for sym in ["<",">","\\","!","#","$","%","^","&","[","]"]:
            input_text=input_text.replace(sym,"")
        return input_text
    else:
        return input_text
def frame_empty():
    data_empty = pd.DataFrame([[""] * 30] * 20)
    column_names = [f'{i + 1}' for i in range(30)]
    data_empty = pd.DataFrame(data_empty, columns=column_names)
    data_empty = data_empty.fillna("")
    return data_empty



def add_new_user(username, password, type_account,project):
    #print("passss:",password)    
    #engine = create_engine("mysql+mysqlconnector://test_user_1:Sql123456@10.192.85.133/db_21xe_clone")
    engine = connect_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    if len(username) < 2 or username.strip() == "":
        session.close()
        return "Username must have at least 2 characters!!!"
    elif len(password) < 6:
        session.close()
        return "Password must have at least 6 characters!!!"
    password=sha256(password.encode('utf-8')).hexdigest()
    result = session.query(User.username).filter_by(username=username).first()
    if result is not None:
        session.close()
        return "Username already exists"
    else:
        user = User(username=username, password=password, permission=type_account,project=project)
        session.add(user)
        session.commit()
        session.close()
        return "Successfully created a new account!!!"
    

def change_password(username, old_password, new_password):
    old_password=sha256(old_password.encode('utf-8')).hexdigest()
    new_password=sha256(new_password.encode('utf-8')).hexdigest()
    #engine = create_engine("mysql+mysqlconnector://test_user_1:Sql123456@10.192.85.133/db_21xe_clone")
    engine = connect_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(User.username, User.password).filter_by(username=username, password = old_password).first()
    if result is None:
        session.close()
        return "Username or password is not correct!!!"
    else:
        if len(new_password) < 6 or new_password.strip() == "":
            session.close()
            return "New password must have at least 6 characters!!!"
        else:
            update_data = {"password": new_password}
            session.query(User).filter(
                (User.username == username) &
                (User.password == old_password)
            ).update(update_data)
            session.commit()
            session.close()
            return "Successfully changed password!!!"
        

def delete_user(df_delete):
    engine = connect_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for index, row in df_delete.iterrows():
        session.query(User.username,User.permission,User.project).filter_by(username=row["username"],permission=row["permission"],project=row["project"]).first()
        session.query(User).filter(User.username == row["username"], User.permission == row["permission"], User.project == row["project"]).delete()
    session.commit()
    session.close()
    return "Successfully deleted user!!!"


#=============================================================================================
def get_all_user(project):
    engine = connect_db()
    #engine = create_engine("mysql+mysqlconnector://test_user_1:Sql123456@10.192.85.133/db_21xe_clone")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(User.username, User.password, User.permission, User.project).all()
    result=pd.DataFrame(result)
    if project!="ALL":
        result=result[(result["project"]==project)]
    # else:
    #     result=result[(result["project"]!=project)]
    
    del result['password']

    return  result

def get_header(project_name, market, powertrain, develop_case):
    #st.title("Cadic program")
    engine = connect_db()
    #engine =create_engine("mysql+mysqlconnector://test_user_1:Sql123456@10.192.85.133/db_21xe_clone")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    project = session.query(Project).filter_by(project_name=project_name, power_train=powertrain, market=market, develop_case=develop_case).first()

    if project is not None:
        id_project = project.id_project
        min_id = session.query(func.min(MainTable.id)).filter(MainTable.id_project == id_project).scalar()
        print("min_id: ", min_id)
        header_query = session.query(Header).filter_by(id_project=id_project).all()
        header_data = [row.__dict__ for row in header_query]
        header_df = pd.DataFrame.from_records(header_data)
        column_order = [column.name for column in Header.__table__.columns]
        header_df = header_df[column_order]
        header_df.drop(['id', 'id_project'], axis=1, inplace=True)
        app_query = session.query(App.market, App.engine, App.gearbox, App.axle, App.handle, App.app).filter_by(project_id = id_project).all()

        app_df = pd.DataFrame(app_query)
        app_df.fillna('')
        app_df_transposed = app_df.transpose()
        app_df_transposed.reset_index(drop=True, inplace=True)

        result_df = pd.concat([header_df, app_df_transposed], axis=1)
        result_df.insert(result_df.shape[1], 'Note_1', '')
        result_df.insert(result_df.shape[1], 'Note_2', '')
        header_df = result_df
        session.close()
        return header_df
    else:
        print("Project not found")



def query_data(project_name, market, powertrain, develop_case, group, lot):
    engine = connect_db()
    group=list_file_by_group(project_name,group)
    #print("xxxxxxxxxxxxxxxx",group)
    #print(project_name, market, powertrain, develop_case, group, lot)
    #engine =create_engine("mysql+mysqlconnector://test_user_1:Sql123456@10.192.85.133/db_21xe_clone")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    project = session.query(Project).filter_by(project_name=project_name, power_train=powertrain, market=market, develop_case=develop_case).first()

    if project is not None:
        id_project = project.id_project
        sum_config = session.query(func.count(App.app)).filter_by(project_id=id_project).first()[0]
        min_id = session.query(func.min(MainTable.id)).filter(MainTable.id_project == id_project).scalar()
        print("min_id: ", min_id)

        header_query = session.query(Header).filter_by(id_project=id_project).all()
        header_data = [row.__dict__ for row in header_query]
        header_df = pd.DataFrame.from_records(header_data)
        column_order = [column.name for column in Header.__table__.columns]
        header_df = header_df[column_order]
        header_df.drop(['id', 'id_project'], axis=1, inplace=True)
        # print("header_df: ", header_df)
        app_query = session.query(App.market, App.engine, App.gearbox, App.axle, App.handle, App.app).filter_by(project_id = id_project).all()

        app_df = pd.DataFrame(app_query)
        app_df.fillna('')
        app_df_transposed = app_df.transpose()
        app_df_transposed.reset_index(drop=True, inplace=True)

        result_df = pd.concat([header_df, app_df_transposed], axis=1)
        result_df.insert(result_df.shape[1], 'Note_1', '')
        result_df.insert(result_df.shape[1], 'Note_2', '')

        main_table_alias = aliased(MainTable)
        columns_to_query = [
            getattr(MainTable, column_name).label(column_name)
            for column_name in columns
        ]
        substring_columns = [
            func.SUBSTRING_INDEX(
                func.SUBSTRING_INDEX(
                    func.GROUP_CONCAT(main_table_alias.value.op('ORDER BY')(main_table_alias.id_app)),
                    ',', counter + 1),
                ',', -1
            )
            for counter in range(0, sum_config)
        ]
        query_data = (
            session.query(*columns_to_query, *substring_columns, MainTable.note_1, MainTable.note_2)
            .join(main_table_alias,
                  MainTable.id == main_table_alias.id)
            .filter(MainTable.id_project == id_project)
        )
        # SUA BAT DAU TU DAY
        group_digital = session.query(MainTable.kca_project_group_digital).group_by(MainTable.kca_project_group_digital).all()
        group_ppc = session.query(MainTable.kca_project_group_ppc).group_by(MainTable.kca_project_group_ppc).all()
        group_ppe = session.query(MainTable.kca_project_group_ppc).group_by(MainTable.kca_project_group_ppc).all()
        all_groups = (*group_digital, *group_ppc, *group_ppe)
        unique_groups_set = set(all_groups)
        unique_groups = tuple(unique_groups_set)
        unique_groups_flat = tuple(item for subtuple in unique_groups for item in subtuple)
        unique_groups_set = set(unique_groups_flat)
        unique_groups_clean = tuple(unique_groups_set)
        if group == "ALL":
            print("thinking.....")
            group = unique_groups_clean
            # print("group: ", group)
        if lot == "DS" or lot == "DC":
            query_data = query_data.filter(MainTable.kca_project_group_digital.in_(group))
        elif lot == "PFC":
            query_data = query_data.filter(MainTable.kca_project_group_ppc.in_(group))
        elif lot == "VC" or lot == "PT1" or lot == "PT2":
            query_data = query_data.filter(MainTable.kca_project_group_ppe.in_(group))
        # KET THUC SUA
        if lot != "ALL":
            lot_lower = lot.lower()
            query_data = query_data.filter(getattr(MainTable, f'evaluate_or_not_{lot_lower}') == 'YES')
        if lot =="ALL":
            query_data = query_data.filter((MainTable.kca_project_group_digital.in_(group))|(MainTable.kca_project_group_ppc.in_(group))|(MainTable.kca_project_group_ppe.in_(group)))
        query_data = query_data.group_by(func.FLOOR((MainTable.id - min_id) / sum_config))

        data_df = pd.read_sql(query_data.statement, session.bind)
        data_df.insert(data_df.columns.get_loc('common_unique') + 1, 'empty_column', '')
        data_df.fillna('', inplace=True)
        data_df.set_index(pd.RangeIndex(start=6, stop=6 + len(data_df)), inplace=True)
        data_df.columns = result_df.columns
        result_df_matched = pd.concat([result_df, data_df], axis=0)
        result_df_matched.columns = range(1, len(result_df_matched.columns) + 1)
        # print("result_df_matched: ", result_df_matched)
        app_alias = aliased(App)
        id_app_list = (
            session.query(app_alias.id_app)
            .filter(app_alias.project_id == id_project)
            .all()
        )
        id_app_list = [row[0] for row in id_app_list]

        if header_df is not None:
            session.close()
            return  session, result_df_matched, id_project, id_app_list
    else:
        session.close()
        st.error("Project not found in the database.")
        return None,frame_empty(),None,None

    
def list_file_by_group(project_name, list_group):
    link_folder = os.path.join('data', project_name)
    list_file = []
    karen_files = [f for f in os.listdir(link_folder) if f.endswith('.xlsx')]
    if "ALL" in list_group:
        list_filename_contain_group = [file_name for file_name in karen_files if "関連表1" in file_name]
        list_file.extend(list_filename_contain_group)

    else:
        for item in list_group:
            list_filename_contain_group = [file_name for file_name in karen_files if item in file_name and "関連表1" in file_name]
            list_file.extend(list_filename_contain_group)

    tuple_group=tuple(list_file)
    return tuple_group



def delete_project(project_name, market, power_train, develop_case):
    engine = connect_db()
    Session = sessionmaker(bind=engine)
    metadata = MetaData()
    metadata.bind = engine
    session = Session()
    project = session.query(Project).filter_by(project_name=project_name, power_train=power_train, market=market,
                                               develop_case=develop_case).first()
    if project is not None:
            session.query(MainTable).filter_by(id_project=project.id_project).delete()
            session.query(App).filter_by(project_id=project.id_project).delete()
            session.query(Header).filter_by(id_project=project.id_project).delete()
            session.delete(project)
            session.commit()
            session.close()
            return "Delete Completed!"
    else:
        session.close()
        return "Project not exist!"