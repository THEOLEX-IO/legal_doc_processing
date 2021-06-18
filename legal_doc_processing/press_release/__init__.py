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
        self.feature_list = [
            "case",
            "cost",
            "date",
            "defendant",
            "id",
            "juridiction",
            "plaintiff",
            "sentence",
            "violation",
        ]

        _ = [setattr(self, k, [(None, -1)]) for k in self.feature_list]

    @property
    def _feature_dict(self):
        return {k: getattr(self, k) for k in self.feature_list}

    @property
    def feature_dict(self):

        clean_l = lambda l: [str(i) for i, j in l]
        return {k: ",".join(clean_l(v)) for k, v in self._feature_dict.items()}

    def predict(self, feature) -> str:
        """ """
        if feature == "case":
            self.case = [(-1, -1)]
            return self.case
        elif feature == "cost":
            self.cost = predict_cost(
                self.struct_text, nlpipe=self.nlpipe, nlspa=self.nlspa
            )
            return self.cost
        elif feature == "date":
            self.date = predict_date(self.struct_text)
            return self.date
        elif feature == "defendant":
            self.defendant = predict_defendant(
                self.struct_text,
                nlpipe=self.nlpipe,
                pers_org_entities_list=self.pers_org_entities_list,
            )
            return self.defendant
        elif feature == "id":
            self.id = predict_id(self.struct_text)
            return self.id
        elif feature == "juridiction":
            self.juridiction = predict_juridiction(
                self.struct_text, nlpipe=self.nlpipe, nlspa=self.nlspa
            )
            return self.juridiction
        elif feature == "plaintiff":
            self.plaintiff = predict_plaintiff(
                self.struct_text, nlpipe=self.nlpipe, nlspa=self.nlspa
            )
            return self.plaintiff
        elif feature == "sentence":
            self.sentence = predict_sentence(
                self.struct_text, nlpipe=self.nlpipe, nlspa=self.nlspa
            )
            return self.sentence
        elif feature == "violation":
            self.violation = predict_violation(
                self.struct_text,
                nlpipe=self.nlpipe,
                pers_org_entities_list=self.pers_org_entities_list,
            )
            return self.violation
        elif feature == "all":
            self.case = [(-1, -1)]
            self.cost = predict_cost(self.struct_text, self.nlpipe, nlspa=self.nlspa)
            self.date = predict_date(self.struct_text)
            self.defendant = predict_defendant(self.struct_text, self.nlpipe)
            self.id = predict_id(self.struct_text)
            self.juridiction = predict_juridiction(
                self.struct_text, self.nlpipe, nlspa=nlspa
            )
            self.plaintiff = predict_plaintiff(self.struct_text, self.nlpipe)
            self.sentence = predict_sentence(self.struct_text, self.nlpipe)
            self.violation = predict_violation(self.struct_text, self.nlpipe)
            return self.feature_dict
        else:
            raise AttributeError("feature Not Implemented")

    def predict_all(self) -> str:
        """return self.predict("all") """

        return self.predict("all")

    def __repr__(self):
        """__repr__ method """

        return f"PressRelease(path:{self.file_path}, file:{self.file_name}, {self._feature_dict}, pipe:{'OK' if self.nlpipe else self.nlpipe})"

    def __str__(self):
        """__str__ method """

        return "a LegalDoc Instance"


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
    one_pr = one.obj
    pred = one_pr.predict_all()

    # for i in range(len(df)):

    #     one = df.iloc[0, :]
    #     one_txt = one.txt
    #     one_pr = one.obj
    #     pred = one_pr.predict_all()
