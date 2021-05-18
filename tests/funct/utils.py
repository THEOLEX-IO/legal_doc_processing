import os
import json

import pandas as pd


root_dir = "./tests/dataset/"
features_root = root_dir + "features/"
labels_root = root_dir + "labels/"


def make_features_dataframe(root=features_root):
    """using all the text files considers as feature, read, build and return a pd.DataFrame object """

    data_list = []
    for text in os.listdir(root):

        with open(root + "/" + text, "r") as f:
            data_list.append({"file_key": text, "text": f.read()})

    return pd.DataFrame(data_list)


def make_labels_dataframe(root=labels_root):
    """using all the json files considers as labels, read, build and return a pd.DataFrame object """

    data_list = []
    for text in os.listdir(root):

        with open(root + "/" + text, "r") as f:
            txt = f.read()
            data_list.append(json.loads(txt))

    return pd.DataFrame(data_list)


def accuracy(list_0: list, list_1: list) -> float:
    """compute basic accuracy score """

    if len(list_0) != len(list_1):
        raise AttributeError("list_0 and list_1 should be same length")

    if type(list_0[0]) != type(list_1[0]):
        raise AttributeError("list_0 and list_1 should be same type")

    return round((sum([tu[0] == tu[1] for tu in zip(list_0, list_1)]) / len(list_0)), 2)
