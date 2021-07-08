import os

from legal_doc_processing import logger

from legal_doc_processing.utils import get_pipeline, get_spacy, get_label_, strize
from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.press_release.structure import structure_press_release
from legal_doc_processing.legal_doc.structure import structure_legal_doc


class BaseData:
    """ container for data """

    def __init__(self):

        pass


class Base:
    """main Base class """

    def __init__(
        self,
        text: str,
        source: str,  # filename OR url with cftc doj ... in
        obj_name: str,  # PressRelesae or LegalDoc or Decision
        # all function could be One line with BasePredict object
        predict_compliance_obligations,
        predict_cooperation_credit,
        predict_court,
        predict_country_of_violation,
        predict_currency,
        predict_decision_date,
        predict_defendant,
        predict_extracted_authorities,
        predict_extracted_violations,
        predict_folder,
        predict_judge,
        predict_justice_type,
        predict_monetary_sanction,
        predict_monitor,
        predict_nature_de_sanction,
        predict_nature_of_violations,
        predict_penalty_details,
        predict_reference,
        predict_type,
        # predict_violation_date,
        nlpipe=None,
        nlspa=None,
    ):
        """ """

        # args check
        juridiction_list = ["cftc", "doj", "sec", "cfbp"]
        juridiction_cands = [i for i in juridiction_list if i in source]
        if not any(juridiction_cands):
            raise AttributeError(f"source arg must refers to one of {juridiction_list}")
        juridiction = juridiction_cands[0]
        obj_name_list = ["PressRelease", "Decision", "LegalDoc"]
        if not obj_name in obj_name_list:
            raise AttributeError(f"obj_name arg must refers to one of {obj_name_list}")

        # args as attr
        self.obj_name = obj_name
        self.juridiction = juridiction
        self.source = source

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

        if obj_name == "PressRelease":

            self.struct_text = structure_press_release(
                text, juridiction=juridiction, nlspa=nlspa
            )
        if obj_name == "LegalDoc":

            self.struct_text = structure_legal_doc(
                text, juridiction=juridiction, nlspa=nlspa
            )
        if obj_name == "Decision":
            self.struct_text = {}

        self.h1 = ""
        self.abstract = ""

        ######################

        # prediction methods
        self._predict = {
            "compliance_obligations": predict_compliance_obligations,
            "cooperation_credit": predict_cooperation_credit,
            "court": predict_court,
            "country_of_violation": predict_country_of_violation,
            "currency": predict_currency,
            "decision_date": predict_decision_date,
            "defendant": predict_defendant,
            "extracted_authorities": predict_extracted_authorities,
            "extracted_violations": predict_extracted_violations,
            "folder": predict_folder,
            "judge": predict_judge,
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

        # WARNING
        # the order of feature in feature list define the order of preidct methods called
        # this order is important
        # ie country of violations depedns of justice_type
        # penalty depends of violations
        self._feature_list = [
            "_cooperation_credit",
            "_court",
            "_decision_date",
            "_extracted_authorities",
            "_extracted_violations",  # ATTENTION PB extracted_violations vs _nature_of violations
            "_folder",
            "_judge",
            "_monitor",
            "_nature_de_sanction",  # attention _penalty_details _monetary_sanction and  _compliance_obligations
            "_nature_of_violations",  ###### ATTENTION PB extracted_violations vs _nature_of violations
            "_reference",
            "_type",  # depends of predict authorities
            "_justice_type",  # depends of predict authorities
            "_defendant",  # depends of _judge and extrcated authorities
            "_country_of_violation",  # depends of predict authorities
            "_currency",  # depends of predict authorities
            "_penalty_details",  # depends of _extracted_violations
            "_monetary_sanction",  # depends of _penalty_details
            "_compliance_obligations",
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
            "source": self.source,
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
    def compliance_obligations(self):
        return strize(self._compliance_obligations)

    @property
    def cooperation_credit(self):
        return strize(self._cooperation_credit)

    @property
    def court(self):
        return strize(self._court)

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
    def extracted_violations(self):
        return strize(self._extracted_violations)

    @property
    def folder(self):
        return strize(self._folder)

    @property
    def judge(self):
        return strize(self._judge)

    @property
    def justice_type(self):
        return strize(self._justice_type)

    @property
    def monetary_sanction(self):
        return strize(self._monetary_sanction)

    @property
    def monitor(self):
        return strize(self._monitor)

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

    # @property
    # def violation_date(self):
    #     return strize(self._violation_date)

    ######################

    def predict(self, feature) -> str:
        """ """

        if feature == "all":
            return self.predict_all()

        # features who needs extracted_authorities
        if feature in [
            "country_of_violation",
            "type",
            "justice_type",
            "country_of_violation",
            "currency",
            "penalty_details",
        ]:
            val = self._predict["extracted_authorities"](self.data)
            setattr(self, "_extracted_authorities", val)

        # Defendant need judge
        if feature == "defendant":
            val = self._predict["judge"](self.data)
            setattr(self, "_judge", val)

        # extracted_violations need penalty_details
        if feature == "penalty_details":
            val = self._predict["extracted_violations"](self.data)
            setattr(self, "_extracted_violations", val)

        if feature in self.feature_list:
            try:
                val = self._predict[feature](self.data)
            except Exception as e:
                val = [("--Error-- " + str(e), -1)]
            setattr(self, "_" + feature, val)
            return val

        return "--Unknowned feature--"

    def predict_all(self) -> str:
        """return self.predict("all") """

        for feature in self.feature_list:
            try:
                val = self._predict[feature](self.data)
            except Exception as e:
                val = [("--Error-- " + str(e), -1)]
            setattr(self, "_" + feature, val)
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
