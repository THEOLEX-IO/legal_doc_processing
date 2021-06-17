import os

from legal_doc_processing.utils import (
    get_pipeline,
    get_spacy,
    _if_not_pipe,
    _if_not_spacy,
)

from legal_doc_processing.legal_doc.case import predict_case
from legal_doc_processing.legal_doc.cost import predict_cost
from legal_doc_processing.legal_doc.date import predict_date
from legal_doc_processing.legal_doc.defendant import predict_defendant
from legal_doc_processing.legal_doc.juridiction import predict_juridiction
from legal_doc_processing.legal_doc.plaintiff import predict_plaintiff
from legal_doc_processing.legal_doc.sentence import predict_sentence
from legal_doc_processing.legal_doc.violation import predict_violation

from legal_doc_processing.legal_doc.structure import structure_legal_doc


class LegalDoc:
    """main legal doc class """

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
            a LegalDoc object"""

        # args as attr
        self.file_path = os.path.dirname(file_path) if file_path else None
        self.file_name = os.path.basename(file_path) if file_path else None
        self.nlpipe = nlpipe if nlpipe else get_pipeline()
        self.nlspa = nlspa if nlspa else get_spacy()

        # text and cleanstructure
        self.raw_text = text
        # self.clean_pages = clean.clean_doc(text)
        # self.structured_text = struct.structure_legal_doc(text)
        self.structured_text = structure_legal_doc(text)
        self.first_page = self.structured_text["pages"][0]

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

    def predict(self, feature) -> str:
        """ """
        if feature == "case":
            self.case = predict_case(self.structured_text)
            return self.case
        elif feature == "cost":
            self.cost = predict_cost(self.first_page, self.nlpipe)
            return self.cost
        elif feature == "date":
            self.date = predict_date(self.first_page)
            return self.date
        elif feature == "defendant":
            self.defendant = predict_defendant(self.first_page, self.nlpipe)
            return self.defendant
        elif feature == "juridiction":
            self.juridiction = predict_juridiction(self.first_page, self.nlpipe)
            return self.juridiction
        elif feature == "plaintiff":
            self.plaintiff = predict_plaintiff(self.first_page, self.nlpipe)
            return self.plaintiff
        elif feature == "sentence":
            self.sentence = predict_sentence(self.first_page, self.nlpipe)
            return self.sentence
        elif feature == "violation":
            self.violation = predict_violation(self.first_page, self.nlpipe)
            return self.violation
        elif feature == "all":
            self.case = predict_case(self.structured_text)
            self.cost = predict_cost(self.first_page, self.nlpipe)
            self.date = predict_date(self.first_page)
            self.defendant = predict_defendant(self.first_page, self.nlpipe)
            self.juridiction = predict_juridiction(self.first_page, self.nlpipe)
            self.plaintiff = predict_plaintiff(self.first_page, self.nlpipe)
            self.sentence = predict_sentence(self.first_page, self.nlpipe)
            self.violation = predict_violation(self.first_page, self.nlpipe)
            return self.feature_dict
        else:
            raise AttributeError("feature Not Implemented")

    def predict_all(self) -> str:
        """return self.predict("all") """

        return self.predict("all")

    def __repr__(self):
        """__repr__ method """

        return f"LegalDoc(raw_text:{self.raw_text[:10]},path:{self.file_path}, file:{self.file_name}, case:{self.case}, defendant:{self.defendant}, pipe:{'OK' if self.nlpipe else self.nlpipe})"

    def __str__(self):
        """__str__ method """

        return "a LegalDoc Instance"


def from_text(text: str, nlpipe=None, nlspa=None):
    """ """

    return LegalDoc(text, nlpipe=nlpipe, nlspa=nlspa)


def from_file(file_path: str, nlpipe=None, nlspa=None):
    """read a file and return a LegalDoc object """

    with open(file_path, "r") as f:
        text = f.read()

    return LegalDoc(text, file_path=file_path, nlpipe=nlpipe, nlspa=nlspa)


if __name__ == "__main__":

    # import
    from legal_doc_processing.legal_doc.utils import legal_doc_X_y
    from legal_doc_processing.legal_doc.structure import (
        structure_legal_doc,
    )

    # laod
    nlpipe = get_pipeline()
    nlpspa = get_spacy()

    # legal_doc structured
    df = legal_doc_X_y()
    df["obj"] = df.txt.apply(lambda i: LegalDoc(i, nlpipe=nlpipe))
    df["header"] = df.obj.apply(lambda i: i.structured_text["header"])
    df["first_page"] = df.obj.apply(lambda i: i.structured_text["pages"][0])

    # # preds
    df["preds"] = df.obj.apply(lambda i: i.predict_all())
    # preds_labels = list(df.preds.iloc[0].keys())
    # for k in preds_labels:
    #     df["pred_" + k] = df.preds.apply(lambda i: i[k])

    # # # 1st one
    # # one = df.iloc[0, :]
    # # one_txt = one.txt
    # # one_ld = one.obj
    # # pred = one_ld.predict_all()

    # _ = [print(i) for i in df.pred_case.values]