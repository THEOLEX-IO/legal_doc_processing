import os
import json

import pytest

from tests.funct.utils import make_features_dataframe, make_labels_dataframe


class TestFeatures:
    """Test class for features"""

    def test_find_features_data(self, root="./tests/dataset/features"):
        """just test to open the files in feature folder"""

        for text in os.listdir(root):

            with open(root + "/" + text, "r") as f:
                txt = f.read()

    def test_make_features_dataframe(self, root="./tests/dataset/features"):
        """using various texts to make a dataframe """

        make_features_dataframe(root)


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

        make_labels_dataframe(root)