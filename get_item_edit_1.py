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


def get_item(data_spec_, list_input_, car_number):

    list_output = []
    dict_output = {}
    # filtered_df is a dataframe containing the filtered options for comparison.
    filtered_df = data_spec_[data_spec_.iloc[:, 3].isin(['optioncode', 'cadics id'])].reset_index(drop=True)
    list_conf_option_code = []
    for column in filtered_df.columns[4:]:
        if pd.notna(filtered_df.at[1, column]):
            list_conf_option_code.append(filtered_df.at[0, column])
    for item in list_input_:
        item_ref = item.copy()
        dict_input = item[-2]
        dict_input=dict(sorted(dict_input.items()))
        conf_check = item[0]
        if conf_check in list_conf_option_code:
            # print("conf_check: ", conf_check)
            # print("dict_input: ", dict_input)
            list_contain_items_config = dict_input.keys()
            filtered_df_list_item = data_spec_[data_spec_.iloc[:, 3].isin(list_contain_items_config)]
            filtered_df_optioncode = filtered_df_list_item[filtered_df_list_item[4 + car_number].notna()]
            filtered_df_optioncode.columns = filtered_df.iloc[0]
            filtered_df_optioncode_w_o = filtered_df_optioncode[filtered_df_optioncode[conf_check] != 'w/o']
            # sub_dict is a dictionary where keys represent the names of options and values represent the equipment,
            # to be merged with dict_input.
            sub_dict = dict(zip(filtered_df_optioncode_w_o.iloc[:, 3],
                                filtered_df_optioncode_w_o.iloc[:, 4 + car_number].apply(lambda x: [x])))
            # Iterate through each key-value pair in dict_input.
            return_dict = {}
            for key, value in dict_input.items():
                # Check whether the key exists in sub_dict.
                if key in sub_dict.keys():
                    # If it exists, combine the value from dict_input and sub_dict.
                    new_key = f"{sub_dict[key][0]}:{key}"
                    return_dict[new_key] = dict_input[key]
                else:
                    # If it doesn't exist, keep the value from dict_input unchanged.
                    return_dict[key] = value
            dict_output = return_dict.copy()
            # list_output.append(dict_output)
            item_ref[-2] = dict_output
        list_output.append(item_ref)
    return list_output


# if __name__ == '__main__':
#     link_spec = r"C:\Users\KNT21617\Documents\Squad4\INPUT_TEST\仕様表_XYZ.xlsx"
#     data_spec = pd.read_excel(link_spec, header=None, sheet_name="Sheet1")
#     data_spec = data_spec.map(lambda x: normalize_japanese_text(x).lower() if isinstance(x, str) else x)
#     list_input = [
#         ['conf-001', 'conf-002', {'op1': ['w/o'], 'op2': ['w/o'], 'op3': ['suv'], 'op4': ['7dq'], 'op5': ['fwd'],
#                                   'op6': ['lhd'], 'op7': ['l1'], 'op8': ['atm (for ev)'], 'op9': ['my00'],
#                                   'op10': ['battery (middle)'], 'op11': ['5'], 'op12': [5], 'op13': ['opt無し']},
#          ', グレード選択: 最上級'],
#         ['conf-003', 'conf-006', {'op1': ['w/o'], 'op2': ['w'], 'op3': ['suv'], 'op4': ['7dq'], 'op5': ['awd'],
#                                   'op6': ['lhd'],
#                                   'op7': ['l3'], 'op8': ['atm (for ev)'], 'op9': ['my00'], 'op10': ['battery (middle)'],
#                                   'op11': ['5'], 'op12': [78], 'op13': ['w/o']}, ', グレード選択: 不問']
#     ]
#     list_return = get_item(data_spec, list_input,
#                            6)  # 6 represents the number of configurations corresponding to car_number.
#     print(list_return)
