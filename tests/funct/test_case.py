import os
import pytest

from tests.funct.utils import (
    make_features_dataframe,
    make_labels_dataframe,
    features_root,
    labels_root,
    accuracy,
)

import legal_doc_processing as ldp


class TestCase:
    """Test class for Case feature"""

    def test_case_accuracy(self, threshold: float = 0.90) -> None:
        """compute accuracy for case prediction; return None """

        # X_test and y_test
        X_test = make_features_dataframe()
        y_test = make_labels_dataframe().reference.values

        # better y_test
        strip_lower = lambda i: str(i).strip().lower()
        y_test = [strip_lower(i) for i in y_test]

        # make pred
        predict = lambda txt: ldp.LegalDoc(txt).predict_case()
        y_pred = [strip_lower(predict(txt)) for txt in X_test.text.values]

        test_vs_pred = list(zip(y_test, y_pred))

        # accuracy
        # assert accuracy(y_test, y_pred) > threshold
