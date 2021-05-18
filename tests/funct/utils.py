import os
import json

import pandas as pd


root_dir = "./tests/dataset/"
features_root = root_dir + "features/"
labels_root = root_dir + "labels/"


def make_features_dataframe(root):
    """using all the text files considers as feature, read, build and return a pd.DataFrame object """

    data_list = []
    for text in os.listdir(root):

        with open(root + "/" + text, "r") as f:
            data_list.append({"file_key": text, "text": f.read()})

    return pd.DataFrame(data_list)


def make_labels_dataframe(root):
    """using all the json files considers as labels, read, build and return a pd.DataFrame object """

    data_list = []
    for text in os.listdir(root):

        with open(root + "/" + text, "r") as f:
            txt = f.read()
            data_list.append(json.loads(txt))

    return pd.DataFrame(data_list)