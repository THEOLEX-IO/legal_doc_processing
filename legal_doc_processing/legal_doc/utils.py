import os
from legal_doc_processing.utils import load_data


def load_legal_doc_files():
    """os list dir files press and .txt """

    # file list
    folder_list = os.listdir("./data/files")
    files_list = [
        [
            f"./data/files/{f}/{i}"
            for i in os.listdir(f"./data/files/{f}")
            if ("press" not in i) and ("txt" in i)
        ]
        for f in folder_list
    ]
    files_list = [i[0] for i in files_list]

    return files_list


def load_legal_doc_text_list():
    """load_legal_doc and load data"""

    files_list = load_legal_doc_files()
    press_txt_list = [load_data(i) for i in files_list]

    return press_txt_list
