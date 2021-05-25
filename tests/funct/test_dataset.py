import os
import json

import pytest

from tests.funct.utils import (
    make_features_dataframe,
    make_labels_dataframe,
    features_root,
    labels_root,
)


class TestFeatures:
    """Test class for features"""

    def test_find_features_data(self, root=features_root):
        """just test to open the files in feature folder"""

        for text in os.listdir(root):

            with open(root + text, "r") as f:
                txt = f.read()

    def test_make_features_dataframe(self, root=features_root):
        """using various texts to make a dataframe """

        make_features_dataframe(root)


class Testlabels:
    """Test class for flabels"""

    def test_find_labels_data(self, root=labels_root):
        """just test to open the files in feature folder"""

        for text in os.listdir(root):

            with open(root + "/" + text, "r") as f:
                txt = f.read()
                js = json.loads(txt)

    def test_make_labels_dataframe(self, root=labels_root):
        """using various texts to make a dataframe """

        make_labels_dataframe(root)