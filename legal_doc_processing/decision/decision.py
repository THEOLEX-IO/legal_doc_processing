import os
import time

from legal_doc_processing.legal_doc import LegalDoc
from legal_doc_processing.press_release import PressRelease

from legal_doc_processing.decision.merge import _merge_ans
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

        # data points private
        self._feature_list = [
            "_case",
            "_cost",
            "_date",
            "_defendant",
            "_id",
            "_juridiction",
            "_plaintiff",
            "_sentence",
            "_violation",
        ]

        self.feature_list = [i[1:] for i in self._feature_list]

        _ = [setattr(self, k, [(None, -1)]) for k in self._feature_list]

    def strize(self, item_list):
        """ """

        clean_l = lambda item_list: [str(i).strip() for i, j in item_list]
        return ",".join(clean_l(item_list))

    @property
    def case(self):
        return self.strize(self._case)

    @property
    def cost(self):
        return self.strize(self._cost)

    @property
    def date(self):
        return self.strize(self._date)

    @property
    def defendant(self):
        return self.strize(self._defendant)

    @property
    def id(self):
        return self.strize(self._id)

    @property
    def juridiction(self):
        return self.strize(self._juridiction)

    @property
    def plaintiff(self):
        return self.strize(self._plaintiff)

    @property
    def sentence(self):
        return self.strize(self._sentence)

    @property
    def violation(self):
        return self.strize("None")

    @property
    def _feature_dict(self):
        return {k: getattr(self, k) for k in self._feature_list}

    @property
    def feature_dict(self):
        return {str(k[1:]): self.strize(getattr(self, k)) for k in self._feature_list}

    def _merge_predictions(self):
        """ """

        del_minus_1 = lambda l: [(i, j) for i, j in l if j >= 0]
        all_preds = {
            k: del_minus_1(self.ld._feature_dict[k] + self.pr._feature_dict[k])
            for k in self._feature_list
        }

        merged_preds = {k: _merge_ans(v) for k, v in all_preds.items()}

        return merged_preds

    def predict_all(self) -> str:
        """return self.predict("all") """

        # do predict
        _ = self.ld.predict_all()
        _ = self.pr.predict_all()

        # merged
        merged_preds = self._merge_predictions()

        # update attrs
        _ = [setattr(self, k, v) for k, v in merged_preds.items()]


def from_text(
    text_ld: str,
    text_pr: str,
    nlpipe=None,
    nlspa=None,
):

    return Decision(text_ld=text_ld, text_pr=text_pr, nlpipe=nlpipe, nlspa=nlspa)


def from_file(
    file_path_ld: str,
    file_path_pr: str,
    nlpipe=None,
    nlspa=None,
):
    """ """

    with open(file_path_ld, "r") as f:
        text_ld = f.read()
    with open(file_path_pr, "r") as f:
        text_pr = f.read()

    return Decision(
        text_ld=text_ld,
        text_pr=text_pr,
        file_path_ld=file_path_ld,
        file_path_pr=file_path_pr,
        nlpipe=nlpipe,
        nlspa=nlspa,
    )


if __name__ == "__main__":

    # import
    import time
    from legal_doc_processing.utils import get_pipeline, get_spacy, get_orgs, get_pers
    from legal_doc_processing.decision.loader import decision_X_y

    # LOAD
    nlpipe = get_pipeline()
    nlspa = get_spacy()

    # df
    merged_df = decision_X_y()

    # objs
    text_pairs = zip(merged_df.press_txt.values, merged_df.legal_txt.values)
    obj_list = [
        Decision(text_pr=i, text_ld=j, nlpipe=nlpipe, nlspa=nlspa) for i, j in text_pairs
    ]
    merged_df["obj"] = obj_list

    # one
    one = merged_df.iloc[0, :]
    self = obj = one.obj

    #
    # self._sub_predict_all()