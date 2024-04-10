import pandas as pd
import unicodedata


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


def get_item(data_spec_, dict_input_, car_number):
    return_dict = {}
    dict_output = dict_input_.copy()
    # filtered_df là dataframe lọc các option cần so sánh.
    filtered_df = data_spec_[data_spec_.iloc[:, 3].isin(['optioncode', 'cadics id'])].reset_index(drop=True)
    # filtered_df.columns = list(data_spec.iloc[0])
    # filtered_df = data_spec[data_spec.iloc[:, 3].eq('OptionCode')]
    # print(filtered_df)
    list_conf_option_code = []
    for column in filtered_df.columns[4:]:
        if pd.notna(filtered_df.at[1, column]):
            list_conf_option_code.append(filtered_df.at[0, column])
    # print("list_conf_option_code: ", list_conf_option_code)
    # list_contain_items_config = []
    for dict_input_key, dict_input_value in dict_input_.items():
        list_split_dict_input_key = dict_input_key.split('_')
        if list_split_dict_input_key[2] in list_conf_option_code:
            # print(list_split_dict_input_key[2])
            list_contain_items_config = dict_input_value.keys()
            # print("data_spec: ", data_spec)
            filtered_df_list_item = data_spec_[data_spec_.iloc[:, 3].isin(list_contain_items_config)]
            filtered_df_optioncode = filtered_df_list_item[filtered_df_list_item[4 + car_number].notna()]
            # sub_dict là 1 dict trong đó key là tên option còn value là các trang bị, để gộp lại với dict_input_value
            sub_dict = dict(zip(filtered_df_optioncode[3], filtered_df_optioncode[4 + car_number].apply(lambda x: [x])))
            # print("sub_dict: ", sub_dict)
            # print("dict_input_value: ", dict_input_value)
            # Duyệt qua từng cặp key-value trong dict_input_value
            for key, value in dict_input_value.items():
                # Kiểm tra xem key có trong sub_dict không
                if key in sub_dict:
                    # Nếu có, kết hợp giá trị từ dict_input_value và sub_dict
                    new_key = f"{sub_dict[key][0]}:{key}"
                    return_dict[new_key] = dict_input_value[key]
                else:
                    # Nếu không, giữ nguyên giá trị từ dict_input_value
                    return_dict[key] = value

            # Duyệt qua các cặp key-value trong sub_dict để kiểm tra các key mới
            # for key, value in sub_dict.items():
            #     if key not in dict_input_value:
            #         return_dict[key] = value
            dict_output[dict_input_key] = return_dict.copy()
    return dict_output


# if __name__ == '__main__':
#     link_spec = r"C:\Users\KNT21617\Documents\Squad4\INPUT_TEST\仕様表_XYZ.xlsx"
#     data_spec = pd.read_excel(link_spec, header=None, sheet_name="Sheet1")
#     data_spec = data_spec.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
#     dict_input = {
#         'US_最上級_conf-001_conf-002': {'op1': ['w/o'], 'op2': ['w/o'], 'op3': ['suv'], 'op4': ['7dq'], 'op5': ['fwd'],
#                                         'op6': ['lhd'], 'op7': ['l1'], 'op8': ['atm (for ev)'], 'op9': ['my00'],
#                                         'op10': ['battery (middle)'], 'op11': ['5'], 'op12': [5], 'op13': ['opt無し']},
#         'US_最上級_conf-003': {'op1': ['w/o'], 'op2': ['w/o'], 'op3': ['suv'], 'op4': ['7dq'], 'op5': ['fwd'],
#                                'op6': ['lhd'],
#                                'op7': ['l1'], 'op8': ['atm (for ev)'], 'op9': ['my00'], 'op10': ['battery (middle)'],
#                                'op11': ['battery (middle)'], 'op12': [5], 'op13': ['opt無し']},
#         'CAN_最上級_conf-004': {'op1': ['w/o'], 'op2': ['w/o'], 'op3': ['suv'], 'op4': ['7dq'], 'op5': ['fwd'],
#                                 'op6': ['lhd'],
#                                 'op7': ['l1'], 'op8': ['atm (for ev)'], 'op9': ['my00'], 'op10': ['battery (middle)'],
#                                 'op11': ['5'], 'op12': [5], 'op13': ['opt無し']},
#         'CAN_最上級_conf-005': {'op1': ['w'], 'op2': ['w'], 'op3': ['suv'], 'op4': ['7dq'], 'op5': ['awd'],
#                                 'op6': ['lhd'],
#                                 'op7': ['l2'], 'op8': ['atm (for ev)'], 'op9': ['my00'], 'op10': ['battery (middle)'],
#                                 'op11': ['5'], 'op12': [27], 'op13': ['opt無し']},
#         'CAN_最上級_conf-006': {'op1': ['w/o'], 'op2': ['w'], 'op3': ['suv'], 'op4': ['7dq'], 'op5': ['awd'],
#                                 'op6': ['lhd'],
#                                 'op7': ['l3'], 'op8': ['atm (for ev)'], 'op9': ['my00'], 'op10': ['battery (middle)'],
#                                 'op11': ['5'], 'op12': [78], 'op13': ['w/o']}}
#     dict_return = get_item(data_spec, dict_input, 6)  # 6 là số conf tương ứng với car_number
#     print(dict_return)
