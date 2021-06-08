import os
from legal_doc_processing.utils import load_data, make_dataframe


def load_legal_doc_files(path="./data/files"):
    """os list dir files press and .txt """

    path = path[:-1] if path[-1] == "/" else path

    # file list
    folder_list = os.listdir(path)
    files_list = [
        [
            f"{path}/{f}/{i}"
            for i in os.listdir(f"{path}/{f}")
            if ("press" not in i) and ("txt" in i)
        ]
        for f in folder_list
    ]
    files_list = [i[0] for i in files_list]

    return files_list


def load_legal_doc_text_list(path="./data/files"):
    """load_legal_doc and load data"""

    files_list = load_legal_doc_files(path)
    press_txt_list = [load_data(i) for i in files_list]

    return press_txt_list


def legal_doc_y_df(path: str = "./data/csv/files.csv", features=None):
    "take data/csv/files.csv, make a df, select press and select releveant features"

    df = make_dataframe(path)
    _df = df.loc[df.doctype != "press", :]
    if not features:
        return _df
    if isinstance(features, str):
        f = [
            "folder",
            "filename",
            features,
        ]
        return _df.loc[:, f]

    if isinstance(features, list):
        f = [
            "folder",
            "filename",
        ]
        f.extend(features)
        return _df.loc[:, f]

    return "--None--"