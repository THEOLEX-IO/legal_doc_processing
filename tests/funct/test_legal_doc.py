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
import legal_doc_processing.information_extraction as infext
import legal_doc_processing.segmentation as seg
import legal_doc_processing.utils as uts


class TestLegalDoc:
    """test class for the LegalDoc object """

    def test_legal_doc_basics(self):
        """test init and basic method of a legal doc oject"""

        # file path
        file_name = os.listdir(features_root)[0]
        file_path = features_root + file_name

        # init object
        lg = ldp.read_file(file_path)

        # case
        assert not lg.case
        assert lg.predict_case()
        assert lg.case
        assert isinstance(lg.case, str)

        # defendant
        assert not lg.defendant
        assert lg.predict_defendant()
        assert lg.defendant
        assert isinstance(lg.defendant, str)

        # predict all
        pred = lg.predict_all()
        assert pred
        assert isinstance(pred, dict)
        assert ("case" in pred.keys()) and ("defendant" in pred.keys())
