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


def check_option_new(df_karen2, data_spec):
    common_dict = {}
    flag_check_empty = False  # No region after 'zone'
    data_spec = data_spec.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
    df_karen2 = df_karen2.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
    # df_karen2 = df_karen2.map(lambda x: normalize_japanese_text(x) if isinstance(x, str) else x)
    list_zone_region_columns = df_karen2.columns[df_karen2.iloc[1].apply(lambda x: str(x)) == 'zone'].tolist()
    df_filter = df_karen2.iloc[1:3, max(list_zone_region_columns) + 1:] if len(
        list_zone_region_columns) > 0 else pd.DataFrame  # after last zone columns
    if df_filter.empty or df_filter.isna().all().all():
        flag_check_empty = True
        # print("DataFrame df_filter is empty.")
    else:
        flag_check_empty = False
        df_filter = df_filter.reset_index(drop=True)
    if flag_check_empty:
        return {}
    else:
        list_option_from_karen2 = list(df_filter.iloc[0, :].drop_duplicates().dropna())
        list_options = df_filter.iloc[0, :].dropna().tolist()
        list_items = df_filter.iloc[1, :].tolist()
        dict_from_karen2 = {}

        for key, value in zip(list_options, list_items):
            if key not in dict_from_karen2:
                dict_from_karen2[key] = []

            if pd.notna(value) and value not in dict_from_karen2[key]:
                dict_from_karen2[key].append(value)
    # print(data_spec)
    filtered_df = data_spec[data_spec.iloc[:, 3].isin(list_option_from_karen2)]
    # print(len(list_option_from_karen2))
    filtered_df.columns = data_spec.iloc[0]

    # list_name_conf là list các config. ví dụ ['conf_001', 'conf_002']
    list_name_conf = filtered_df.columns.dropna().tolist()[4:]
    # sub_dict là dict tạo bởi: Key là giá trị trong cột 'cadics id' ; value trong các cột conf tương ứng
    sub_dict = {}
    # result_dict là output trong đó key là tên các conf ví dụ 'conf_001" value là dict tương ứng conf trong syo
    result_dict = {}
    for column in list_name_conf:
        sub_dict = dict(zip(filtered_df['cadics id'], filtered_df[column].apply(lambda x: [x])))
        dict_from_karen2 = replace_standard(dict_from_karen2)
        sub_dict = replace_standard(sub_dict)
        common_dict = common_elements(sub_dict, dict_from_karen2)
        # flag_check_dict là biến bool check xem các option thỏa maxn hay không.
        flag_check_dict = False

        # So sánh dict_common với sub_dict (dict tạo với các conf)
        if common_dict == sub_dict:
            flag_check_dict = True
        for key in result_dict.keys():

            # Tìm vị trí chữ 'c' cuối cùng trong key
            last_c_index = key.rfind('c')

            # Chỉ lấy cột cuối
            last_column_in_pair = key[last_c_index:]
            if (filtered_df[column] == filtered_df[last_column_in_pair]).all():
                # Nối các conf nếu chúng có các option giống hệt nhau
                key_merge = key + "_" + column

                # Sau khi nối xong thì thay key cũ bằng key mới.
                result_dict[key_merge] = result_dict.pop(key)
                flag_check_dict = False
                break
        if flag_check_dict:
            result_dict[column] = sub_dict
    return result_dict


if __name__ == '__main__':
    link_karen2 = r"C:\NO1_FINAL\data\OneDrive_1_2024-3-27\関連表2_I(WHハーネス)_XX4.xlsx"
    link_spec = r"C:\NO1_FINAL\data\OneDrive_1_2024-3-27\仕様表_WZ1J.xlsx"
    data_spec = pd.read_excel(link_spec, header=None, sheet_name="Sheet1")
    df_karen2 = pd.read_excel(link_karen2, sheet_name="関連表", header=None)
    time1 = time.time()
    end = check_option_new(df_karen2, data_spec)
    time2 = time.time()
    # print("xxxxxx",len(end))
    print('Runtime: ', time2 - time1)
