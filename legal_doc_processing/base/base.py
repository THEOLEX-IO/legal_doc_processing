import os

from legal_doc_processing.utils import get_pipeline, get_spacy, get_label_, strize

from legal_doc_processing.utils import uniquize as _u

# from legal_doc_processing.utils import load_data


class Base:
    """main Base class """

    def __init__(
        self,
        text: str,
        obj_name: str,
        doctype: str,
        structure_method,
        predict_code_law_violation,
        predict_country_of_violation,
        predict_currency,
        predict_decision_date,
        predict_defendant,
        predict_extracted_authorities,
        predict_extracted_violation,
        predict_folder,
        predict_justice_type,
        predict_monetary_sanction,
        predict_monitor,
        predict_nature_de_sanction,
        predict_nature_of_violations,
        predict_penalty_details,
        predict_reference,
        predict_type,
        # predict_violation_date,
        file_path: str = None,
        nlpipe=None,
        nlspa=None,
    ):
        """ """

        # args as attr
        self.obj_name = obj_name
        self.doctype = doctype
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

        # prediction methods
        self._predict = {
            "code_law_violation": predict_code_law_violation,
            "country_of_violation": predict_country_of_violation,
            "currency": predict_currency,
            "decision_date": predict_decision_date,
            "defendant": predict_defendant,
            "extracted_authorities": predict_extracted_authorities,
            "extracted_violation": predict_extracted_violation,
            "folder": predict_folder,
            "justice_type": predict_justice_type,
            "monetary_sanction": predict_monetary_sanction,
            "monitor": predict_monitor,
            "nature_de_sanction": predict_nature_de_sanction,
            "nature_of_violations": predict_nature_of_violations,
            "penalty_details": predict_penalty_details,
            "reference": predict_reference,
            "type": predict_type,
            # "violation_date ": predict_violation_date,
        }

        ######################

        # text and clean
        self.raw_text = text
        self.struct_text = structure_method(text)
        self.h1 = ""
        self.abstract = ""

        ######################

        # WARNING
        # the order of feature in feature list define the order of preidct methods called
        # this order is important
        # ie country of violation depedns of justice_type
        # penalty depends of violations
        self._feature_list = [
            "_code_law_violation",
            "_currency",
            "_decision_date",
            "_defendant",
            "_extracted_authorities",
            "_extracted_violation",
            "_folder",
            "_justice_type",
            "_monitor",
            "_nature_de_sanction",
            "_nature_of_violations",
            "_reference",
            "_type",
            "_country_of_violation",  # depends of predict authorities
            "_penalty_details",  # depends of _extracted_violation
            "_monetary_sanction",  # depends of _penalty_details
            # depends of predict authorities
            # "_violation_date",
        ]

        self.feature_list = [i[1:] for i in self._feature_list]
        _ = [setattr(self, k, [(None, -1)]) for k in self._feature_list]

    ######################

    @property
    def _feature_dict(self):
        return {k: getattr(self, k) for k in self._feature_list}

    @property
    def feature_dict(self):
        return {str(k[1:]): strize(getattr(self, k)) for k in self._feature_list}

    @property
    def data(self):
        """ """

        dd = {
            # pipe spacy
            "nlpipe": self.nlpipe,
            "nlspa": self.nlspa,
            # feature
            "_feature_dict": self._feature_dict,
            "feature_dict": self.feature_dict,
            # text
            "raw_text": self.raw_text,
            "struct_text": self.struct_text,
            "h1": self.h1,
            "abstract": self.abstract,
            # sents
            "h1_sents": self.h1_sents,
            "abstract_sents": self.abstract_sents,
            "all_text_sents": self.all_text_sents,
            # entities
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

        return dd

    ######################

    def set_all(self):
        """ """

        # self._set_entities() / entities
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

        # self.sents() / sents
        self.h1_sents = [i.text for i in self.nlspa(self.h1).sents if i.text.strip()]
        self.abstract_sents = [
            i.text for i in self.nlspa(self.abstract).sents if i.text.strip()
        ]
        self.all_text_sents = []

    ######################

    @property
    def code_law_violation(self):
        return strize(self._code_law_violation)

    @property
    def country_of_violation(self):
        return strize(self._country_of_violation)

    @property
    def currency(self):
        return strize(self._currency)

    @property
    def decision_date(self):
        return strize(self._decision_date)

    @property
    def defendant(self):
        return strize(self._defendant)

    @property
    def extracted_authorities(self):
        return strize(self._extracted_authorities)

    @property
    def extracted_violation(self):
        return strize(self._extracted_violation)

    @property
    def folder(self):
        return strize(self._folder)

    @property
    def justice_type(self):
        return strize(self._justice_type)

    @property
    def monetary_sanction(self):
        return strize(self._monetary_sanction)

    @property
    def nature_de_sanction(self):
        return strize(self._nature_de_sanction)

    @property
    def nature_of_violations(self):
        return strize(self._nature_of_violations)

    @property
    def penalty_details(self):
        return strize(self._penalty_details)

    @property
    def reference(self):
        return strize(self._reference)

    @property
    def type(self):
        return strize(self._type)

    @property
    def violation_date(self):
        return strize(self._violation_date)

    ######################

    def predict(self, feature) -> str:
        """ """

        if feature == "all":
            return self.predict_all()

        # extracted_violation need penalty_details
        if feature == "penalty_details":
            val = self._predict["extracted_violation"](self.data)
            setattr(self, "_extracted_violation", val)

        if feature in self.feature_list:
            # try:
            val = self._predict[feature](self.data)
            setattr(self, "_" + feature, val)
            return val
            # except:
            #     return "--Error--"
        return "--Unknowned feature--"

    def predict_all(self) -> str:
        """return self.predict("all") """

        for feature in self.feature_list:
            setattr(self, "_" + feature, self._predict[feature](self.data))

        # DEPRECATED
        # self._code_law_violation = self._predict["code_law_violation"](self.data)
        # self._country_of_violation = self._predict["country_of_violation"](self.data)
        # self._currency = self._predict["currency"](self.data)
        # self._decision_date = self._predict["decision_date"](self.data)
        # self._defendant = self._predict["defendant"](self.data)
        # self._extracted_authorities = self._predict["extracted_authorities"](self.data)
        # self._id = self._predict["id"](self.data)
        # self._juridiction = self._predict["juridiction"](self.data)
        # self._monetary_sanction = self._predict["monetary_sanction"](self.data)
        # self._nature_of_violations = self._predict["nature_of_violations"](self.data)
        # self._plaintiff = self._predict["plaintiff"](self.data)
        # self._reference = self._predict["reference"](self.data)
        # self._sentence = self._predict["sentence"](self.data)
        # # self._violation_date = self._predict["violation_date"](self.data)

        return self.feature_dict

    ######################

    def __repr__(self):
        """__repr__ method """

        _pipe = "OK" if self.nlpipe else self.nlpipe
        _spa = "OK" if self.nlspa else self.nlspa
        _feat_dict = {k: v[:8] for k, v in self.feature_dict.items()}
        return f"{self.obj_name}(path:{self.file_path}, file:{self.file_name}, {_feat_dict}, pipe/spacy:{_pipe}/{_spa}"

    def __str__(self):
        """__str__ method """

        return self.__repr__()


def base_from_text(text: str, Object, nlpipe=None, nlspa=None):
    """ """

    try:
        return Object(text, nlpipe=nlpipe, nlspa=nlspa)
    except Exception as e:
        return e.__str__()


def base_from_file(file_path: str, Object, nlpipe=None, nlspa=None):
    """read a file and return  object """

    try:
        with open(file_path, "r") as f:
            text = f.read()
    except Exception as e:
        return e.__str__()

    return Object(text, file_path=file_path, nlpipe=nlpipe, nlspa=nlspa)
