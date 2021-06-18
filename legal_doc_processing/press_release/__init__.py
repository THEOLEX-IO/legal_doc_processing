import os

from legal_doc_processing.utils import get_pipeline, get_spacy

# from legal_doc_processing.utils import load_data

from legal_doc_processing.press_release.cost import predict_cost
from legal_doc_processing.press_release.date import predict_date
from legal_doc_processing.press_release.defendant import predict_defendant
from legal_doc_processing.press_release.id import predict_id
from legal_doc_processing.press_release.juridiction import predict_juridiction
from legal_doc_processing.press_release.plaintiff import predict_plaintiff
from legal_doc_processing.press_release.sentence import predict_sentence
from legal_doc_processing.press_release.structure import structure_press_release
from legal_doc_processing.press_release.violation import predict_violation

from legal_doc_processing.press_release.utils import get_entities_pers_orgs

# from legal_doc_processing.press_release.loader import (
#     load_press_release_files,
#     load_press_release_text_list,
# )


class PressRelease:
    """main press release doc class """

    def __init__(
        self,
        text: str,
        file_path: str = None,
        nlpipe=None,
        nlspa=None,
    ):
        """init method of the LegalDoc
        pos args :
            text (str) : the complete text to proceed
            nlpipe (pipleline) : a pre instanciated pipline. default None (a object will be created)
        opt args :
            -
        raise :
            -
        return :
            a Press Release object"""

        # args as attr
        self.file_path = os.path.dirname(file_path) if file_path else None
        self.file_name = os.path.basename(file_path) if file_path else None

        self.nlpipe = nlpipe if nlpipe else get_pipeline()
        self.nlspa = nlspa if nlspa else get_spacy()

        # text and clean
        self.raw_text = text
        self.struct_text = structure_press_release(text)

        # entities
        self.pers_org_entities_list = get_entities_pers_orgs(self.struct_text)

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

    def predict(self, feature) -> str:
        """ """

        if feature == "case":
            self._case = [(-1, -1)]
            return self._case
        elif feature == "cost":
            self._cost = predict_cost(
                self.struct_text, nlpipe=self.nlpipe, nlspa=self.nlspa
            )
            return self._cost
        elif feature == "date":
            self._date = predict_date(self.struct_text)
            return self._date
        elif feature == "defendant":
            self._defendant = predict_defendant(
                self.struct_text,
                nlpipe=self.nlpipe,
                pers_org_entities_list=self.pers_org_entities_list,
            )
            return self._defendant
        elif feature == "id":
            self._id = predict_id(self.struct_text)
            return self._id
        elif feature == "juridiction":
            self._juridiction = predict_juridiction(
                self.struct_text, nlpipe=self.nlpipe, nlspa=self.nlspa
            )
            return self._juridiction
        elif feature == "plaintiff":
            self._plaintiff = predict_plaintiff(
                self.struct_text, nlpipe=self.nlpipe, nlspa=self.nlspa
            )
            return self._plaintiff
        elif feature == "sentence":
            self._sentence = predict_sentence(
                self.struct_text, nlpipe=self.nlpipe, nlspa=self.nlspa
            )
            return self._sentence
        elif feature == "violation":
            self._violation = predict_violation(
                self.struct_text,
                nlpipe=self.nlpipe,
                pers_org_entities_list=self.pers_org_entities_list,
            )
            return self._violation
        elif feature == "all":
            self._case = [(-1, -1)]
            self._cost = predict_cost(self.struct_text, self.nlpipe, nlspa=self.nlspa)
            self._date = predict_date(self.struct_text)
            self._defendant = predict_defendant(self.struct_text, self.nlpipe)
            self._id = predict_id(self.struct_text)
            self._juridiction = predict_juridiction(
                self.struct_text, self.nlpipe, nlspa=nlspa
            )
            self._plaintiff = predict_plaintiff(self.struct_text, self.nlpipe)
            self._sentence = predict_sentence(self.struct_text, self.nlpipe)
            self._violation = predict_violation(self.struct_text, self.nlpipe)
            return self._feature_dict
        else:
            raise AttributeError("feature Not Implemented")

    def predict_all(self) -> str:
        """return self.predict("all") """

        return self.predict("all")

    def __repr__(self):
        """__repr__ method """

        _pipe = "OK" if self.nlpipe else self.nlpipe
        _spa = "OK" if self.nlspa else self.nlspa
        _feat_dict = {k: v[:8] for k, v in self.feature_dict.items()}
        return f"PressRelease(path:{self.file_path}, file:{self.file_name}, {_feat_dict}, pipe/spacy:{_pipe}/{_spa}"

    def __str__(self):
        """__str__ method """

        return self.__repr__()


def from_text(text: str, nlpipe=None, nlspa=None):
    """ """

    return PressRelease(text, nlpipe=nlpipe, nlspa=nlspa)


def from_file(file_path: str, nlpipe=None, nlspa=None):
    """read a file and return a PressRelease object """

    with open(file_path, "r") as f:
        text = f.read()

    return PressRelease(text, file_path=file_path, nlpipe=nlpipe, nlspa=None)


if __name__ == "__main__":

    # import
    import time
    from legal_doc_processing.utils import get_pipeline, get_spacy, get_orgs, get_pers
    from legal_doc_processing.press_release.loader import press_release_X_y
    from legal_doc_processing.press_release.structure import structure_press_release

    # LOAD
    nlpipe = get_pipeline()
    nlspa = get_spacy()

    # legal_doc df AND  OBj
    df = press_release_X_y()
    df = df.iloc[:4, :]
    df["obj"] = df.txt.apply(lambda i: PressRelease(i, nlpipe=nlpipe, nlspa=nlspa))

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["preds"] = df.obj.apply(lambda i: i.predict_all())
    t = time.time() - t

    # labels
    preds_labels = list(df.preds.iloc[0].keys())
    for k in preds_labels:
        df["pred_" + k] = df.preds.apply(lambda i: i[k])

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    self = one_pr = one.obj
    pred = one_pr.predict_all()

    # for i in range(len(df)):

    #     one = df.iloc[0, :]
    #     one_txt = one.txt
    #     one_pr = one.obj
    #     pred = one_pr.predict_all()
