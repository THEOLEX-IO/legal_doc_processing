import os

import pandas as pd

from legal_doc_processing.utils import load_data, make_dataframe


# def load_press_release_files(path="./data/files"):
#     """os list dir files press and .txt """

#     path = path[:-1] if path[-1] == "/" else path

#     # file list
#     folder_list = os.listdir(path)
#     files_list = [
#         [
#             f"{path}/{f}/{i}"
#             for i in os.listdir(f"{path}/{f}")
#             if ("press" in i) and ("txt" in i)
#         ]
#         for f in folder_list
#     ]
#     files_list = [i[0] for i in files_list]

#     return files_list


# def load_press_release_text_list(path="./data/files"):
#     """load_press_release_files and load data"""

#     files_list = load_press_release_files(path)
#     press_txt_list = [load_data(i) for i in files_list]

#     return press_txt_list


def press_release_X_df(
    path: str = "./data/csv/", y: str = "random_y", text: str = "random_text"
) -> pd.DataFrame:
    """ """

    cands = os.listdir(path)
    text_file = [i for i in cands if text in i][0]
    y_file = [i for i in cands if y in i][0]

    text_df = pd.read_csv(path + text_file)
    y_df = pd.read_csv(path + y_file)

    drop_cols = [i for i in y_df.columns if "link" in i]
    y_df.drop(drop_cols, axis=1, inplace=True)

    new_df = text_df.merge(y_df, on="folder", how="inner", copy=True)

    return pd.DataFrame(df)


def press_release_y_df(path: str = "./data/csv/files.csv", features=None):
    "take data/csv/files.csv, make a df, select press and select releveant features"

    df = make_dataframe(path)
    _df = df.loc[df.doctype == "press", :]
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


def press_release_X_y(root: str = "./data", features=None):
    """df X and df y, merge and return  """

    # clean root
    root = root[:-1] if root[-1] == "/" else root

    # init X and y
    X = press_release_X_df(f"{root}/files")
    y = press_release_y_df(f"{root}/csv/files.csv", features)

    # be sure same length
    assert len(X) == len(y)

    # drop filename
    X.drop("filename", axis=1, inplace=True)
    y.drop("filename", axis=1, inplace=True)

    # merge
    X_y = pd.merge(X, y, how="inner", on="folder")

    # same length
    assert len(X_y) == len(X)

    X_y = X_y.sort_values("folder", ascending=True)
    X_y.index = range(len(X_y))

    return X_y