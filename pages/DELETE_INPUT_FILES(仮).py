import os
import streamlit as st


# 指定されたフォルダ内のファイルを取得する関数
def get_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    return files


# ファイルを削除する関数
def delete_files(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            st.success(f"ファイル {file_path} を削除しました。")
        else:
            st.error(f"ファイル {file_path} が見つかりませんでした。")


# Streamlitアプリケーションのセットアップ
def main():
    st.title("Inputファイル削除ページ")
    st.caption('こちらのページはトライアル用に削除をしやすくするために用意しました。')

    folder_list = [
        folder
        for folder in os.listdir("./data")
        if not folder.startswith(".") and not "list_acc.json" in folder
    ]
    selected_folder = st.selectbox("削除するフォルダを選択してください:", folder_list)

    # 選択されたフォルダのパスを作成
    folder_path = os.path.join("./data", selected_folder)

    # 選択されたフォルダ内のファイルを取得
    files = get_files_in_folder(folder_path)

    # ファイルを選択して削除
    files_to_delete = st.multiselect("削除するファイルを選択してください:", files)

    # 選択されたファイルのフルパスを作成
    file_paths = [os.path.join(folder_path, file) for file in files_to_delete]

    # ファイルが選択された場合、削除ボタンを表示
    if st.button("選択されたファイルを削除"):
        delete_files(file_paths)


if __name__ == "__main__":
    try:
        if st.session_state.position!="staff":
            try:
                main()
            except:
                st.warning("Input is empty!")
        else:
            st.warning("Permission Deny!")
    except:
        st.warning("Please login before running app!!!")
