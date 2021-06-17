import os
import time

from legal_doc_processing.legal_doc import LegalDoc
from legal_doc_processing.press_release import PressRelease

from legal_doc_processing.utils import (
    get_pipeline,
    get_spacy,
    _if_not_pipe,
    _if_not_spacy,
)


class Decision:
    """main Decision  class """

    def __init__(
        self,
        text_ld: str,
        text_pr: str,
        file_path_ld: str = None,
        file_path_pr: str = None,
        nlpipe=None,
        nlspa=None,
    ):

        # args as attr
        self.file_path_ld = os.path.dirname(file_path_ld) if file_path_ld else None
        self.file_path_pr = os.path.basename(file_path_pr) if file_path_pr else None
        self.nlpipe = nlpipe if nlpipe else get_pipeline()
        self.nlspa = nlspa if nlspa else get_spacy()

        # sub objects
        self.ld = LegalDoc(text_ld, nlpipe=nlpipe, nlspa=nlspa)
        self.pr = PressRelease(text_pr, nlpipe=nlpipe, nlspa=nlspa)

        # features / data points
        self.feature_list = [
            "id",
            "case",
            "cost",
            "date",
            "defendant",
            "plaintiff",
            "sentence",
            "juridiction",
            "violation",
        ]

        _ = [setattr(self, k, None) for k in self.feature_list]

    @property
    def feature_dict(self):
        return {k: getattr(self, k) for k in self.feature_list}

    def _sub_predict_all(self) -> str:
        """return self.predict("all") """

        self.ld_preds = self.ld.predict_all()
        self.pr_preds = self.pr.predict_all()

        return {"ld_preds": self.ld_preds, "pr_preds": self.pr_preds}
