import os
import json

import pytest
import pandas as pd


def test_find_features_data(root="./tests/dataset/features"):
    """just test to open the files in feature folder"""

    for text in os.listdir(root):

        with open(root + "/" + text, "r") as f:
            txt = f.read()


def test_make_features_dataframe(root="./tests/dataset/features"):
    """using various texts to make a dataframe """

    data_list = []
    for text in os.listdir(root):

        with open(root + "/" + text, "r") as f:
            data_list.append({"file_key": text, "text": f.read()})

        df = pd.DataFrame(data_list)

    return df


def test_find_features_labels(root="./tests/dataset/labels"):
    """just test to open the files in feature folder"""

    for text in os.listdir(root):

        with open(root + "/" + text, "r") as f:
            txt = f.read()
            js = json.loads(txt)


def test_make_labels_dataframe(root="./tests/dataset/labels"):
    """using various texts to make a dataframe """

    data_list = []
    for text in os.listdir(root):

        with open(root + "/" + text, "r") as f:
            txt = f.read()
            data_list.append(json.loads(txt))

        df = pd.DataFrame(data_list)

    return df