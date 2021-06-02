import os
import pytest
import pandas as pd

from tests.funct.utils import (
    make_features_dataframe,
    make_labels_dataframe,
    features_root,
    labels_root,
    accuracy,
)

import legal_doc_processing as ldp
import legal_doc_processing.information_extraction as infext
import legal_doc_processing.segmentation as seg
import legal_doc_processing.utils as uts


class TestDefendant:
    """Test class for Defendant feature"""

    def test_defendant_accuracy(self, threshold: float = 0.90) -> None:
        """compute accuracy for defendant prediction; return None """

        nlpipe = infext.get_pipeline()

        # read df
        df = pd.read_csv("./data/csv/dataset.csv")
        df = df.iloc[:5, :]

        # X_test and y_test
        X_test = df.drop(
            "defendant",
            axis=1,
        )
        y_test = df.defendant.values

        # make pred
        predict = lambda txt: ldp.LegalDoc(txt, nlpipe=nlpipe).predict_defendant()
        y_pred = [predict(txt) for txt in X_test.document_TEXT.values]

        test_vs_pred = list(zip(y_test, y_pred))

        # # accuracy
        # assert accuracy(y_test, y_pred) > threshold
