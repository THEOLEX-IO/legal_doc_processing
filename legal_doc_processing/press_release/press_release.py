import os

from legal_doc_processing.utils import get_pipeline, get_spacy, get_label_

from legal_doc_processing.utils import uniquize as _u

# from legal_doc_processing.utils import load_data

from legal_doc_processing.press_release.monetary_sanction import predict_monetary_sanction
from legal_doc_processing.press_release.decision_date import predict_decision_date
from legal_doc_processing.press_release.defendant import predict_defendant
from legal_doc_processing.press_release.id import predict_id
from legal_doc_processing.press_release.extracted_authorities import (
    predict_extracted_authorities,
)
from legal_doc_processing.press_release.plaintiff import predict_plaintiff
from legal_doc_processing.press_release.sentence import predict_sentence
from legal_doc_processing.press_release.structure import structure_press_release
from legal_doc_processing.press_release.nature_of_violations import (
    predict_nature_of_violations,
)
from legal_doc_processing.press_release.currency import predict_currency

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
        n_paragraphs=4,
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

        # pipe and spacy
        self.nlpipe = nlpipe if nlpipe else get_pipeline()
        self.nlspa = nlspa if nlspa else get_spacy()
        try:
            self.nlspa.add_pipe("sentencizer")
        except Exception as e:
            pass

        ######################

        # text and clean
        self.raw_text = text
        self.struct_text = structure_press_release(text)
        self.h1 = self.struct_text["h1"]
        self.sub_article = "\n".join(
            self.struct_text["article"].split("\n")[:n_paragraphs]
        )

        self.h1_sents = [i.txt for i in nlspa(self.h1).sents]
        self.sub_article_sents = [i.text for i in nlspa(self.sub_article).sents]

        ######################

        # entities
        self.pers_h1 = _u(get_label_(self.h1, "PERSON", self.nlspa))
        self.pers_sub_article = _u(get_label_(self.sub_article, "PERSON", self.nlspa))
        self.org_h1 = _u(get_label_(self.h1, "ORG", self.nlspa))
        self.org_sub_article = _u(get_label_(self.sub_article, "ORG", self.nlspa))
        self.date_h1 = _u(get_label_(self.h1, "DATE", self.nlspa))
        self.date_sub_article = _u(get_label_(self.sub_article, "DATE", self.nlspa))
        self.cost_h1 = _u(get_label_(self.h1, "MONEY", self.nlspa))
        self.cost_sub_article = _u(self.get_label_(self.sub_article, "MONEY", self.nlspa))
        # all
        self.pers_all = _u(self.pers_h1 + self.pers_sub_article)
        self.org_all = _u(self.org_h1 + self.org_sub_article)
        self.pers_org_all = _u(self.pers_all + self.org_all)
        self.date_all = _u(self.date_h1 + self.date_sub_article)
        self.cost_all = _u(self.cost_h1 + self.cost_sub_article)

        ######################

        # data points private
        self._feature_list = [
            "_currency",
            "_code_law_violation",
            "_country_of_violation",
            "_decision_date",
            "_defendant",
            "_extracted_authorities",
            "_id",
            "_juridiction",
            "_monetary_sanction",
            "_nature_of_violations",
            "_plaintiff",
            "_reference",
            "_sentence",
            "_violation_date",
        ]
        self.feature_list = [i[1:] for i in self._feature_list]

        _ = [setattr(self, k, [(None, -1)]) for k in self._feature_list]

    ######################

    def strize(self, item_list):
        """ """

        clean_l = lambda item_list: [str(i).strip() for i, j in item_list]
        return ",".join(clean_l(item_list))

    ######################

    @property
    def currency(self):
        return self.strize(self._currency)

    @property
    def code_law_violation(self):
        return self.strize(self._code_law_violation)

    @property
    def country_of_violation(self):
        return self.strize(self._country_of_violation)

    @property
    def decision_date(self):
        return self.strize(self._decision_date)

    @property
    def defendant(self):
        return self.strize(self._defendant)

    @property
    def extracted_authorities(self):
        return self.strize(self._extracted_authorities)

    @property
    def id(self):
        return self.strize(self._id)

    @property
    def juridiction(self):
        return self.strize(self._juridiction)

    @property
    def monetary_sanction(self):
        return self.strize(self._monetary_sanction)

    @property
    def nature_of_violations(self):
        return self.strize(_nature_of_violations)

    @property
    def plaintiff(self):
        return self.strize(self._plaintiff)

    @property
    def reference(self):
        return self.strize(self._reference)

    @property
    def sentence(self):
        return self.strize(self._sentence)

    @property
    def violation_date(self):
        return self.strize(self._violation_date)

    ######################

    @property
    def _feature_dict(self):
        return {k: getattr(self, k) for k in self._feature_list}

    @property
    def feature_dict(self):
        return {str(k[1:]): self.strize(getattr(self, k)) for k in self._feature_list}

    ######################

    def predict(self, feature) -> str:
        """ """
        if feature != "all":
            raise NotImplementedError("sorry, method not supported")
        else:
            self._currency = predict_currency(self.struct_text)
            self._code_law_violation = predict_code_law_violation(self.struct_text)
            self._country_of_violation = predict_country_of_violation(self.struct_text)

            self._reference = [(-1, -1)]

            self._monetary_sanction = predict_monetary_sanction(
                self.struct_text, self.nlpipe, nlspa=self.nlspa
            )
            self._decision_date = predict_decision_date(self.struct_text)
            self._defendant = predict_defendant(self.struct_text, self.nlpipe)
            self._id = predict_id(self.struct_text)
            self._extracted_authorities = predict_extracted_authorities(
                self.struct_text, self.nlpipe, nlspa=self.nlspa
            )
            self._plaintiff = predict_plaintiff(self.struct_text, self.nlpipe)
            self._sentence = predict_sentence(self.struct_text, self.nlpipe)
            self._nature_of_violations = predict_nature_of_violations(
                self.struct_text, self.nlpipe
            )

            return self.feature_dict
        else:
            raise AttributeError("feature Not Implemented")

    def predict_all(self) -> str:
        """return self.predict("all") """

        return self.predict("all")

    ######################

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
    try:
        return PressRelease(text, nlpipe=nlpipe, nlspa=nlspa)
    except Exception as e:
        return e.__str__()


def from_file(file_path: str, nlpipe=None, nlspa=None):
    """read a file and return a PressRelease object """

    try:
        with open(file_path, "r") as f:
            text = f.read()
    except Exception as e:
        return e.__str__()

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
    one_ob = one.obj
    one_pred = one.preds
