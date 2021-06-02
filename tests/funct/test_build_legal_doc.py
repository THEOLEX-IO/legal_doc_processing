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


class TestLegalDoc:
    """test class for the LegalDoc object """

    def test_legal_doc_basics(self):
        """test init and basic method of a legal doc oject"""

        # # file path
        # file_name = os.listdir(features_root)[0]
        # file_path = features_root + file_name

        # # init object
        # ld = ldp.read_file(file_path)

        df = pd.read_csv("./data/csv/dataset.csv")
        txt = df.loc[0, "document_TEXT"]
        ld = ldp.LegalDoc(txt)

        # case
        assert not ld.case
        assert ld.predict_case()
        assert ld.case
        assert isinstance(ld.case, str)

        # defendant
        assert not ld.defendant
        assert ld.predict_defendant()
        assert ld.defendant
        assert isinstance(ld.defendant, str)

        # predict all
        pred = ld.predict_all()
        assert pred
        assert isinstance(pred, dict)
        assert ("case" in pred.keys()) and ("defendant" in pred.keys())
