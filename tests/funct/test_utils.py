import pytest

from tests.funct.utils import (
    make_features_dataframe,
    make_labels_dataframe,
    features_root,
    labels_root,
    accuracy,
)


class TestAccuracy:
    """test accuracy is good """

    def test_basic_accuracy_pass(self):
        """test basic configuration where accuracy is ok """

        l_0 = ["a", "b", "c"]
        l_1 = ["a", "b", "c"]

        assert accuracy(l_0, l_1) > 0.99

        l_0 = ["a", "b", "ce"]
        l_1 = ["a", "b", "c"]

        assert accuracy(l_0, l_1) > 0.66

        l_0 = ["a", "bi", "ce"]
        l_1 = ["a", "b", "c"]

        assert accuracy(l_0, l_1) > 0.32

        l_0 = ["ap", "bi", "ce"]
        l_1 = ["a", "b", "c"]

        assert accuracy(l_0, l_1) < 0.01

    def test_basic_accuracy_fail(self):
        """test basic configuration where test fail"""

        l_0 = [1, "b", "ce"]
        l_1 = ["a", "b", "c"]

        with pytest.raises(AttributeError):
            accuracy(l_0, l_1)

        l_0 = ["a", "b"]
        l_1 = ["a", "b", "c"]

        with pytest.raises(AttributeError):
            accuracy(l_0, l_1)
