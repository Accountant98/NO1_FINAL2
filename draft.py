import pandas as pd

list_input_ = [['conf-003',
                {'front windscreen heater / heated front screen': ['w/o'], 'srvm': ['w'], 'antenna': ['shark fin'],
                 'audio & navigation / types of radios': ['s'], 'ad2': ['w']}, 'グレード選択: 最上級'], ['conf-006', {
    'front windscreen heater / heated front screen': ['w/o'], 'srvm': ['w/o'], 'antenna': ['shark fin'],
    'audio & navigation / types of radios': ['s'], 'ad2': ['w']}, 'グレード選択: 最上級']]
list_conf_option_code = ['conf-003', 'conf-006']
data_spec_ = pd.read_excel(r"C:\Users\KNT21617\Downloads\New folder (5)\NO1_FINAL\data\WZ1J\仕様表_WZ1J.xlsx")
filtered_df = data_spec_[data_spec_.iloc[:, 3].isin(['optioncode', 'cadics id'])].reset_index(drop=True)

return_dict = {}
list_output = []
dict_output = {}
for item in list_input_:
    # print("item: ", item)
    item_ref = item.copy()
    dict_input = item[-2]
    dict_input = dict(sorted(dict_input.items()))
    conf_check = item[0]
    if conf_check in list_conf_option_code:
        # print("conf_check: ", conf_check)
        # print("dict_input: ", dict_input)
        list_contain_items_config = dict_input.keys()
        filtered_df_list_item = data_spec_[data_spec_.iloc[:, 3].isin(list_contain_items_config)]
        # print("filtered_df_list_item ",filtered_df_list_item)
        filtered_df_optioncode = filtered_df_list_item[filtered_df_list_item.iloc[:,10].notna()]
        filtered_df_optioncode.columns = filtered_df.iloc[0]
        # print("filtered_df_optioncode: ", filtered_df_optioncode)
        filtered_df_optioncode_w_o = filtered_df_optioncode[filtered_df_optioncode[conf_check] != 'w/o']
        # print("filtered_df_optioncode_w_o:", filtered_df_optioncode_w_o)
        # sub_dict is a dictionary where keys represent the names of options and values represent the equipment,
        # to be merged with dict_input.
        sub_dict = dict(zip(filtered_df_optioncode_w_o.iloc[:, 3],
                            filtered_df_optioncode_w_o.iloc[:, 4 + 6].apply(lambda x: [x])))
        # print("subdict: ", sub_dict)
        # print("dict_input: ", dict_input)

        # Iterate through each key-value pair in dict_input.
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
        # print("dict_output: ", dict_output)

        item_ref[-2] = dict_output
    list_output.append(item_ref)
# print("list_output: ", list_output)
# print("*****************************************************************")

