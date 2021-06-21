import os

from legal_doc_processing.utils import get_pipeline, get_spacy, get_label_

from legal_doc_processing.utils import uniquize as _u

# from legal_doc_processing.utils import load_data


class Base:
    """main Base class """

    def __init__(
        self,
        text: str,
        obj_name: str,
        structure_method,
        predict_currency,
        predict_code_law_violation,
        predict_country_of_violation,
        predict_decision_date,
        predict_defendant,
        predict_extracted_authorities,
        predict_id,
        predict_juridiction,
        predict_monetary_sanction,
        predict_nature_of_violations,
        predict_plaintiff,
        predict_reference,
        predict_sentence,
        predict_violation_date,
        file_path: str = None,
        nlpipe=None,
        nlspa=None,
    ):
        """ """

        # args as attr
        self.obj_name = ""
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
        self.struct_text = structure_method(text)
        self.h1 = ""
        self.abstract = ""

        ######################

    def set_features(self):
        """ """

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

    def set_entities(self):
        """ """

        # entities
        self.pers_h1 = _u(get_label_(self.h1, "PERSON", self.nlspa))
        self.pers_abstract = _u(get_label_(self.abstract, "PERSON", self.nlspa))
        self.org_h1 = _u(get_label_(self.h1, "ORG", self.nlspa))
        self.org_abstract = _u(get_label_(self.abstract, "ORG", self.nlspa))
        self.date_h1 = _u(get_label_(self.h1, "DATE", self.nlspa))
        self.date_abstract = _u(get_label_(self.abstract, "DATE", self.nlspa))
        self.cost_h1 = _u(get_label_(self.h1, "MONEY", self.nlspa))
        self.cost_abstract = _u(get_label_(self.abstract, "MONEY", self.nlspa))

        # all
        self.pers_all = _u(self.pers_h1 + self.pers_abstract)
        self.org_all = _u(self.org_h1 + self.org_abstract)
        self.pers_org_all = _u(self.pers_all + self.org_all)
        self.date_all = _u(self.date_h1 + self.date_abstract)
        self.cost_all = _u(self.cost_h1 + self.cost_abstract)

    def set_data_collection(self):
        """ """

        self.data_ = {
            "_feature_dict": self._feature_dict(),
            "feature_dict": self.feature_dict(),
            "nlpipe": self.nlpipe,
            "nlspa": self.nlspa,
            "raw_text": self.raw_text,
            "struct_text": self.struct_text,
            "h1": self.h1,
            "abstract": self.abstract,
            "pers_h1": self.pers_h1,
            "pers_abstract": self.pers_abstract,
            "org_h1": self.org_h1,
            "org_abstract": self.org_abstract,
            "date_h1": self.date_h1,
            "date_abstract": self.date_abstract,
            "cost_h1": self.cost_h1,
            "cost_abstract": self.cost_abstract,
            "pers_all": self.pers_all,
            "org_all": self.org_all,
            "pers_org_all": self.pers_org_all,
            "date_all": self.date_all,
            "cost_all": self.cost_all,
        }

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
        return self.strize(self._nature_of_violations)

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
            self._currency = predict_currency(self.data_)
            self._code_law_violation = predict_code_law_violation(self.data_)
            self._country_of_violation = predict_country_of_violation(self.data_)
            self._decision_date = predict_decision_date(self.data_)
            self._defendant = predict_defendant(self.data_)
            self._extracted_authorities = predict_extracted_authorities(self.data_)
            self._id = predict_id(self.data_)
            self._juridiction = predict_juridiction(self.data_)
            self._monetary_sanction = predict_monetary_sanction(self.data_)
            self._nature_of_violations = predict_nature_of_violations(self.data_)
            self._plaintiff = predict_plaintiff(self.data_)
            self._reference = predict_reference(self.data_)
            self._sentence = predict_sentence(self.data_)
            self._violation_date = predict_violation_date(self.data_)

            return self.feature_dict

    def predict_all(self) -> str:
        """return self.predict("all") """

        return self.predict("all")

    ######################

    def __repr__(self):
        """__repr__ method """

        _pipe = "OK" if self.nlpipe else self.nlpipe
        _spa = "OK" if self.nlspa else self.nlspa
        _feat_dict = {k: v[:8] for k, v in self.feature_dict.items()}
        return f"(path:{self.file_path}, file:{self.file_name}, {_feat_dict}, pipe/spacy:{_pipe}/{_spa}"

    def __str__(self):
        """__str__ method """

        return self.__repr__()


def from_text(text: str, Object, nlpipe=None, nlspa=None):
    """ """
    try:
        return Object(text, nlpipe=nlpipe, nlspa=nlspa)
    except Exception as e:
        return e.__str__()


def from_file(file_path: str, Object, nlpipe=None, nlspa=None):
    """read a file and return  object """

    try:
        with open(file_path, "r") as f:
            text = f.read()
    except Exception as e:
        return e.__str__()

    return Object(text, file_path=file_path, nlpipe=nlpipe, nlspa=None)
