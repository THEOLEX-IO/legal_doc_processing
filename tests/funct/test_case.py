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

    def test_case_work(self):
        """just test predict defendant is ok """

        # file path
        file_name = os.listdir(features_root)[0]
        file_path = features_root + file_name

        # init object
        lg = ldp.read_file(file_path)

    def test_case_accuracy(self, threshold: float = 0.90) -> None:
        """compute accuracy for case prediction; return None """

        # X_test and y_test
        X_test = make_features_dataframe()
        # y_test = make_labels_dataframe().case.values

        y_pred = [predict(txt) for txt in X_test.text.values]

        # # make pred
        # predict = lambda txt: ldp.LegalDoc(txt).predict_defendant()
        # y_pred = [predict(txt) for txt in X_test.text.values]

        # test_vs_pred = list(zip(y_test, y_pred))

        # # # accuracy
        # # assert accuracy(y_test, y_pred) > threshold
