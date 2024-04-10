import pandas as pd
import unicodedata
import time


def normalize_japanese_text(input_text):
    normalized_text = ''
    if isinstance(input_text, str):

        for char in input_text:
            normalized_char = unicodedata.normalize('NFKC', char)
            normalized_text += normalized_char
        normalized_text = normalized_text.replace("\n", "")
        normalized_text = normalized_text.strip()
        return normalized_text
    else:
        return input_text


"""
Name function: common_elements
Combine two dictionaries
input: dict_karen(dict): Dictionary of karenhyo2, dict_syo(dict): Dictionary of syo
output: common_dict (dict):  New dictionary after Combined
"""


def common_elements(dict_syo, dict_kanren):
    common_dict = {}
    for key, values2 in dict_kanren.items():
        if 'all' in values2 or 'All' in values2:
            common_values = dict_syo[key]
        else:
            list_item_in_karen = dict_syo[key].copy()
            list_item_in_syo = values2.copy()

            if "w" in list_item_in_syo:
                list_item_in_karen = [value for value in list_item_in_karen if value != "w/o"]
                list_item_in_syo.remove("w")
                list_item_in_syo.extend(list_item_in_karen)

            common_values = list(set(dict_syo[key]) & set(list_item_in_syo))

        common_dict[key] = common_values

    return common_dict


"""
Name function: replace_standard
replace special characters
input: dict_need_to_replace(dict): Dictionary of equipment, list_same_mean(list): Equipment with the same mean
output: new_dict_replaced (dict):  New dictionary after being replaced
"""


def replace_standard(dict_need_to_replace):
    list_same_mean = [['w/o', 'without', '-'], ['w', 'with'], ['other', 'その他'], ['awd', '4wd'], ['fwd', '2wd']]
    new_dict_replaced = dict_need_to_replace.copy()

    for key, value_list in dict_need_to_replace.items():
        for i in range(len(value_list)):
            for sublist in list_same_mean:
                if value_list[i] in sublist:
                    new_dict_replaced[key][i] = sublist[0]
                    break
    return new_dict_replaced


def check_option_new(df_karen2, data_spec, df_input, dict_input):
    result_dict = {}
    data_spec = data_spec.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
    df_input = df_input.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)

    list_option_from_karen2 = list(df_input.iloc[0, :].drop_duplicates().dropna())
    # print("list_option_from_karen2: ", list_option_from_karen2)
    list_options = list(df_input.iloc[0, :].dropna())
    # print("list_options: ", list_options)
    list_items = df_input.iloc[1, :].tolist()
    # print("list_items: ", list_items)
    list_conditions = df_input.iloc[2, :].tolist()
    # print("list_conditions: ", list_conditions)
    dict_items_from_karen2 = {}

    for key_sub, value in zip(list_options, list_items):
        if key_sub not in dict_items_from_karen2:
            dict_items_from_karen2[key_sub] = []

        if pd.notna(value) and value not in dict_items_from_karen2[key_sub]:
            dict_items_from_karen2[key_sub].append(value)
    dict_conditions_from_karen2 = {}
    for key_sub, value in zip(list_options, list_conditions):
        if key_sub not in dict_conditions_from_karen2:
            dict_conditions_from_karen2[key_sub] = []
        if pd.notna(value) and value not in dict_conditions_from_karen2[key_sub]:
            dict_conditions_from_karen2[key_sub].append(value)

    # Trường hợp ['最上級'] và ['最下級'] cùng tồn tại là vô lý. trả về dict rỗng.
    if ['最上級'] in dict_conditions_from_karen2.values() and ['最下級'] in dict_conditions_from_karen2.values():
        return {}
    # print("dict_items_from_karen2: ", dict_items_from_karen2)
    # print("dict_conditions_from_karen2: ", dict_conditions_from_karen2)
    # print("list_option_from_karen2: ", list_option_from_karen2)

    # filtered_df là dataframe lọc các option cần so sánh.
    filtered_df = data_spec[data_spec.iloc[:, 3].isin(list_option_from_karen2)]
    # print("filtered_df: ", filtered_df)
    # Tạo tên cột để bước sau tạo dict. Cột 'cadics id' là key và các cột còn lại (lần lượt) làm value
    filtered_df.columns = data_spec.iloc[0]

    for condition, list_name_conf in dict_input.items():
        if [condition.split('_')[-1]] not in dict_conditions_from_karen2.values():
            continue
        # list_name_conf là list các config. ví dụ ['conf_001', 'conf_002']
        # sub_dict là dict tạo bởi: Key là giá trị trong cột 'cadics id' ; value trong các cột conf tương ứng
        sub_dict = {}
        # result_dict là output trong đó key là tên các conf ví dụ 'conf_001" value là dict tương ứng conf trong syo

        for column in list_name_conf:
            # tạo dict. Cột 'cadics id' là key và các cột còn lại (lần lượt) làm value
            sub_dict = dict(zip(filtered_df['cadics id'], filtered_df[column].apply(lambda x: [x])))
            # Chuẩn hóa cc kí tự
            dict_items_from_karen2 = replace_standard(dict_items_from_karen2)
            # sub_dict = replace_standard(sub_dict)
            if not sub_dict or len(sub_dict) != len(dict_items_from_karen2):
                return {}
            # print("sub_dict: ", sub_dict)
            # print("dict_items_from_karen2: ", dict_items_from_karen2)
            # Tìm dict giao nhau
            common_dict = common_elements(sub_dict, dict_items_from_karen2)
            # flag_check_dict là biến bool check xem các option thỏa mãn hay không.
            flag_check_dict = False
            #
            """
            So sánh dict_common với sub_dict (dict tạo với các conf) nếu giống nhau thì xem trong dict kết quả có cột 
            nào giống không? nếu cóp th ch việc thêm vào cuối, nếu không có hoặc không trùng dict thì tạo mới 
            """
            if common_dict == sub_dict:
                flag_check_dict = True
            for key_sub in result_dict.keys():

                # Tìm vị trí chữ 'c' cuối cùng trong key
                last_c_index = key_sub.rfind('c')

                # Chỉ lấy cột cuối ví dụ chuỗi 'US_最上級_conf-001_conf-002' thì lấy 'conf-002'
                last_column_in_pair = key_sub[last_c_index:]

                # Nếu cột giống nhau và nằm trong cùng zone key thì thêm vào key
                if (filtered_df[column] == filtered_df[
                    last_column_in_pair]).all() and last_column_in_pair in list_name_conf and condition in key_sub:
                    # Nối các conf nếu chúng có các option giống hệt nhau
                    key_merge = key_sub + "_" + column

                    # Sau khi nối xong thì thay key cũ bằng key mới.
                    result_dict[key_merge] = result_dict.pop(key_sub)
                    flag_check_dict = False
                    break
            if flag_check_dict:
                result_dict[condition + "_" + column] = sub_dict
    return result_dict


# if __name__ == '__main__':
#     link_karen2 = r"C:\Users\KNT21617\Downloads\New folder (5)\NO1_FINAL\data\WZ1J\関連表2_A(コントロール)_XR2.xlsx"
#     link_spec = r"C:\Users\KNT21617\Downloads\New folder (5)\NO1_FINAL\data\xx4ハーネス\xx4ハーネス\仕様表_WZ1J.xlsx"
#     data_spec = pd.read_excel(link_spec, header=None, sheet_name="Sheet1")
#     df_karen2 = pd.read_excel(link_karen2, sheet_name="関連表", header=None)
#     df_input = df_karen2.iloc[1:4, 24:35]
#     print("df_input: ", df_input)
#     dict_input_1 = {'US_最上級': ['conf-001', 'conf-002', 'conf-003'],
#                     'CAN_最上級': ['conf-004', 'conf-005', 'conf-006']}
#
#     dict_input = {'us_不問': ['conf-003', 'conf-001']}
#     time1 = time.time()
#     dict_output = check_option_new(df_karen2, data_spec, df_input, dict_input)
#     print(dict_output)
#     # print("dict_output: ", dict_output)
#     time2 = time.time()
#     print('Runtime: ', time2 - time1)
