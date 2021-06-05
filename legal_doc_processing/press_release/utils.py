import os
from legal_doc_processing.utils import load_data


def load_press_release_text_list():
    """os list dir files press and .txt """

    # file list
    folder_list = os.listdir("./data/files")
    files_list = [
        [
            f"./data/files/{f}/{i}"
            for i in os.listdir(f"./data/files/{f}")
            if ("press" in i) and ("txt" in i)
        ]
        for f in folder_list
    ]
    files_list = [i[0] for i in files_list]

    # load all press release
    press_txt_list = [load_data(i) for i in files_list]

    return press_txt_list
