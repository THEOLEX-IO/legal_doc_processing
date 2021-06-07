import os
from legal_doc_processing.utils import load_data


def load_press_release_files(path="./data/files"):
    """os list dir files press and .txt """

    path = path[:-1] if path[-1] == "/" else path

    # file list
    folder_list = os.listdir(path)
    files_list = [
        [
            f"{path}/{f}/{i}"
            for i in os.listdir(f"{path}/{f}")
            if ("press" in i) and ("txt" in i)
        ]
        for f in folder_list
    ]
    files_list = [i[0] for i in files_list]

    return files_list


def load_press_release_text_list(path="./data/files"):
    """load_press_release_files and load data"""

    files_list = load_press_release_files(path)
    press_txt_list = [load_data(i) for i in files_list]

    return press_txt_list