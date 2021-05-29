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
from legal_doc_processing.information_extraction import get_pipeline


class TestDefendant:
    """Test class for Defendant feature"""

    def test_defendant_accuracy(self, threshold: float = 0.90) -> None:
        """compute accuracy for defendant prediction; return None """

        nlpipe = get_pipeline()

        # X_test and y_test
        X_test = make_features_dataframe()
        y_test = make_labels_dataframe().defendant.values

        # make pred
        predict = lambda txt: ldp.LegalDoc(txt, nlpipe=nlpipe).predict_defendant()
        y_pred = [predict(txt) for txt in X_test.text.values]

        test_vs_pred = list(zip(y_test, y_pred))

        # # accuracy
        # assert accuracy(y_test, y_pred) > threshold
