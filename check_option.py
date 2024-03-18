"""Create by KD.Trong - KNT21617 17:00:00 - 07/12/2023"""
"""Update by KD.Trong - KNT21617 17:00:00 - 08/12/2023"""
"""Update by KD.Trong - KNT21617 13:45:00 - 11/12/2023"""
"""Update by KD.Trong - KNT21617 14:45:00 - 18/12/2023"""
import pandas as pd
import unicodedata

"""
Name function: create_no_zone_dataframe
Create dataframe for "zone"
input: df (dataframe)
ouput: result_df (dataframe):  DataFrame don't contain the "zone" column.
"""


def create_no_zone_dataframe(df_1):
    flag_check_empty = False
    df_1 = df_1.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
    matching_columns = df_1.columns[df_1.iloc[1].apply(lambda x: str(x).lower()) == 'zone'].tolist()
    data_test = df_1.iloc[1:3, max(matching_columns) + 1:]
    if data_test.empty or data_test.isna().all().all():
        flag_check_empty = True
        result_df = data_test
    else:
        flag_check_empty = False
        data_test.iloc[0] = data_test.iloc[0].str.strip()
        result_df = data_test.reset_index(drop=True)
    return result_df, flag_check_empty


"""
Name function: create_df_feature
Create dictionary for future
input: df_temp (dataframe) DataFrame don't contain the "zone" column.
ouput: df (dataframe):  DataFrame of feature
"""


def create_df_feature(df_temp):
    df_x = df_temp.iloc[0, :]
    df = df_x.drop_duplicates()
    df = pd.DataFrame(df).reset_index(drop=True).dropna()
    # print(df)
    return df


"""
Name function: create_dict_from_kanrenhyo2
Create dictionaries from kanrenhyo2
input: df1 (dataframe), df2 (dataframe)
ouput: result_dict (dict):  Equipment in kanrenhyo2
"""


def create_dict_from_kanrenhyo2(df1, df2):
    result_dict = {}
    for value in df1.loc[:, 0]:
        if value in df2.iloc[0].values:
            find_result = df2.columns[df2.iloc[0] == value].tolist()
            result_dict[value] = [df2.loc[1, i] for i in find_result if pd.notna(df2.loc[1, i])]
        else:
            result_dict[value] = []
    return result_dict


"""
Name function: create_dict_from_syo
Create dictionaries from syo
input: df1 (dataframe):key, df2 (dataframe): equipment
ouput: result_dict (dict):  Equipment in syo
"""


def create_dict_from_syo(df, file_spec):
    data_spec_ = pd.read_excel(file_spec, sheet_name="Sheet1", header=None)
    data_spec_ = data_spec_.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
    # df = df.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
    data_spec_.iloc[:, 3] = data_spec_.iloc[:, 3].str.strip()
    List_dict = {}
    for index, value in df[0].items():
        rows_with_value = data_spec_.index[data_spec_[3] == value.strip()]
        List_value = []
        if not rows_with_value.empty:
            List_value.append(data_spec_.iloc[rows_with_value[0], 5])
            for i in range(1, 5):
                x = data_spec_.iloc[rows_with_value[0], 5 + i]
                if x not in List_value:
                    List_value.append(x)
            # List_dict.append({value: List_value})
            List_dict[value] = List_value
        else:
            # print(f"Value '{value}' not found in data_spec_.")
            List_dict[value] = []
    return List_dict


"""
Name function: repalce_symbol
replace special characters
input: dict(dict): Dictionary of equipment, list(list): Equipment with the same symbol
ouput: new_dict (dict):  New dictionary after being replaced
"""


def repalce_symbol(dict, list):
    new_dict = dict.copy()
    for key, value_list in dict.items():
        for i in range(len(value_list)):
            for sublist in list:
                if value_list[i] in sublist:
                    new_dict[key][i] = sublist[0]
                    break
    return new_dict


"""
Name function: common_elements
Combine two dictionaries
input: dict1(dict): Dictionary of kanrenhyo2, dict2(dict): Dictionary of syo
ouput: common_dict (dict):  New dictionary after Combined
"""


def common_elements(dict1, dict2):
    common_dict = {}

    for key in dict2.keys():
        list_temp = []
        if 'all' in dict2.get(key):
            common_values = dict1[key]
        else:
            list_1 = dict1[key].copy()
            list_2 = dict2[key].copy()
            if "w" in list_2:
                try:
                    list_1.remove("w/o")
                except:
                    None
                list_2.remove("w")
                list_2 = list_2 + list_1
            dict2[key] = list_2
            common_values = list(set(dict1[key]) & set(dict2.get(key, [])))

        common_dict[key] = common_values

    return common_dict


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


def create_string(result_dict_replace, common_dict, result_dict, List_dict_replce):
    for item1, item2, item3 in zip(common_dict, result_dict_replace, List_dict_replce):
        if common_dict[item1] == List_dict_replce[item3] or 'all' in result_dict_replace[item2]:
            result_dict.pop(item1)
    
    return result_dict
    # str_comment = str(result_dict)
    # for sym in ["[", "]", "'", "{", "}"]:
    #     str_comment = str_comment.replace(sym, "")
    # return str_comment


def check_option(df_1, file_spec):
    result_dict = {}
    List_dict = {}
    common_dict = {}
    flag_check_empty = False
    super_list = [['w/o', 'without', '-'], ['w', 'with'], ['other', 'その他'], ['awd', '4wd'], ['fwd', '2wd']]
    df_temp, flag_check_empty = create_no_zone_dataframe(df_1)
    if flag_check_empty:
        return common_dict,1
    else:
        df = create_df_feature(df_temp)
        result_dict = create_dict_from_kanrenhyo2(df, df_temp)
        List_dict = create_dict_from_syo(df, file_spec)
        List_dict_replce = repalce_symbol(List_dict, super_list)
        result_dict_replace = repalce_symbol(result_dict, super_list)
        common_dict = common_elements(List_dict_replce, result_dict_replace)
        dict_kep = create_string(result_dict_replace, common_dict, result_dict, List_dict_replce)
        # print("List_dict_replce: ", List_dict_replce)
        # print("result_dict_replace: ", result_dict_replace)
        # print("common_dict: ", common_dict)
        return common_dict, dict_kep


# df_1 = pd.read_excel(
#     r"\\vn-ntv-fs004ada\SAVE-DATA\03. XQZ\No1_プロ管集約業務の一本化\05.WORK\DEV\TRONG\27 thang 2\関連表2_I(HF-VR-ETC)_XM6.xlsx",
#     header=None)
# df_1 = df_1.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
# file_spec = r"\\vn-ntv-fs004ada\SAVE-DATA\03. XQZ\No1_プロ管集約業務の一本化\05.WORK\DEV\TRONG\27 thang 2\仕様表_YYYY.xlsx"

# dict_return, cmt_string = check_option(df_1, file_spec)
# print("cmt_string: ", cmt_string)
# print("*********")
