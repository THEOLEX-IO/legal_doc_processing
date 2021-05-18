import pytest

from tests.funct.utils import (
    make_features_dataframe,
    make_labels_dataframe,
    features_root,
    labels_root,
    accuracy,
)


class TestDefendant:
    """Test class for Defendant feature"""

    def test_defendant_accuracy(self, threshold: float = 0.90) -> None:
        """compute accuracy for defendant prediction; return None """

        # X_test and y_test
        X_test = make_features_dataframe()
        y_test = make_labels_dataframe().defendant.values

        # make pred
        y_pred = [
            "",
        ] * len(y_test)

        assert accuracy(y_test, y_pred) > threshold
