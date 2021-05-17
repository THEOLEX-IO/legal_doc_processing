import os
import json

import pytest
import pandas as pd


class TestFeatures:
    """Test class for features"""

    def test_find_features_data(self, root="./tests/dataset/features"):
        """just test to open the files in feature folder"""

        for text in os.listdir(root):

            with open(root + "/" + text, "r") as f:
                txt = f.read()

    def test_make_features_dataframe(self, root="./tests/dataset/features"):
        """using various texts to make a dataframe """

        data_list = []
        for text in os.listdir(root):

            with open(root + "/" + text, "r") as f:
                data_list.append({"file_key": text, "text": f.read()})

            df = pd.DataFrame(data_list)

        return df


class Testlabels:
    """Test class for flabels"""

    def test_find_labels_data(self, root="./tests/dataset/labels"):
        """just test to open the files in feature folder"""

        for text in os.listdir(root):

            with open(root + "/" + text, "r") as f:
                txt = f.read()
                js = json.loads(txt)

    def test_make_labels_dataframe(self, root="./tests/dataset/labels"):
        """using various texts to make a dataframe """

        data_list = []
        for text in os.listdir(root):

            with open(root + "/" + text, "r") as f:
                txt = f.read()
                data_list.append(json.loads(txt))

            df = pd.DataFrame(data_list)

        return df