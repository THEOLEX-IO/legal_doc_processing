import os

import requests

from legal_doc_processing import logger

from legal_doc_processing.utils import get_pipeline, get_spacy, get_label_, strize
from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.press_release.structure import structure_press_release
from legal_doc_processing.legal_doc.structure import structure_legal_doc

from legal_doc_processing.base.predict_handler import predict_handler
from legal_doc_processing.base.data_handler import DataHandler


class Base:
    """main Base class """

    def __init__(
        self,
        text: str,
        source: str,  # filename OR url with cftc doj ... in
        obj_name: str,  # PressRelesae or LegalDoc or Decision
        nlpipe=None,
        nlspa=None,
        abstract_n_lines=5,
    ):
        """ """

        # args check
        juridiction_list = ["cftc", "doj", "sec", "cfbp", "cfpb"]
        juridiction_cands = [i for i in juridiction_list if i in source]
        if not any(juridiction_cands):
            raise AttributeError(f"source arg must refers to one of {juridiction_list}")
        juridiction = juridiction_cands[0].strip().lower()
        obj_name_list = ["PressRelease", "Decision", "LegalDoc"]
        if not obj_name in obj_name_list:
            raise AttributeError(f"obj_name arg must refers to one of {obj_name_list}")

        # args as attr
        self.obj_name = obj_name
        self.juridiction = juridiction
        self.source = source

        # text
        self.raw_text = text
        self.date = ""
        self.h1 = ""
        self.header = ""
        self.content = ""
        self.struct_content = ""
        self.abstract = ""
        self.end = ""

        # pipe and spacy
        self.nlpipe = nlpipe if nlpipe else get_pipeline()
        self.nlspa = nlspa if nlspa else get_spacy()

        ######################

        # structure doc
        if obj_name == "PressRelease":

            struct_text = structure_press_release(
                text, juridiction=juridiction, nlspa=nlspa
            )
            self.date = struct_text["date"]
            self.h1 = struct_text["h1"]
            self.header = ""
            self.content = struct_text["article"]
            self.abstract = "\n".join(
                struct_text["article"].splitlines()[:abstract_n_lines]
            )

        elif obj_name == "LegalDoc":
            self.struct_text = structure_legal_doc(text, juridiction=juridiction, nlspa=nlspa)

        elif obj_name == "Decision":
            self.struct_text = {}

        ######################

        # prediction methods
        self._predict = predict_handler(obj_name)

        ######################

        # WARNING
        # the order of feature in feature list define the order of preidct methods called
        # this order is important
        # ie country of violations depedns of justice_type
        # penalty depends of violations

        # predict_country_of_violation NEED extracted_authorities
        # predict_extracted_authorities NEEDS judge
        # Justice_type NEEDS extracted_authorities

        self._feature_list = [
            "_cooperation_credit",
            "_court",
            "_currency",
            "_decision_date",
            "_extracted_sanctions",
            "_extracted_violations",  # ATTENTION PB extracted_violations vs _nature_of violations
            "_folder",
            "_judge",
            "_monitor",
            "_nature_de_sanction",  # _nature_de_sanction needs_extracted_sanctions
            "_nature_of_violations",  ###### ATTENTION PB extracted_violations vs _nature_of violations
            "_reference",
            "_extracted_authorities",  # depends of judge
            "_type",  # depends of _extracted_authorities
            "_justice_type",  # depends of _extracted_authorities
            "_defendant",  # depends of _judge and _extracted_authorities
            "_country_of_violation",  # depends of _extracted_authorities
            "_penalty_details",  # depends of _extracted_sanctions
            "_monetary_sanction",  # depends of _penalty_details
            "_compliance_obligations",  # depends of _extracted_sanctions
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
        return DataHandler(self)

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
        self.content_sents = [
            i.text for i in self.nlspa(self.content).sents if i.text.strip()
        ]

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
        ]:
            val = self._predict["extracted_authorities"](self.data)
            setattr(self, "_extracted_authorities", val)

        # Defendant need judge
        if feature == "defendant":
            val = self._predict["judge"](self.data)
            setattr(self, "_judge", val)

        # nature_de_sanction, penalty_details need extracted_sanctions
        if feature == "nature_de_sanction":
            val = self._predict["extracted_sanctions"](self.data)
            setattr(self, "_extracted_sanctions", val)

        if feature == "penalty_details":
            val = self._predict["extracted_sanctions"](self.data)
            setattr(self, "_extracted_sanctions", val)

        if feature in self.feature_list:
            try:
                val = self._predict[feature](self.data)
            except Exception as e:
                val = [("--Error-- " + str(e), 1)]
            setattr(self, "_" + feature, val)
            return val

        return AttributeError(f"Unknowned feature : {feature} ")

    def predict_all(self) -> str:
        """return self.predict("all") """

        for feature in self.feature_list:
            try:
                val = self._predict[feature](self.data)
            except Exception as e:
                val = [("--Error-- " + str(e), 1)]
            setattr(self, "_" + feature, val)
        return self.feature_dict

    ######################

    def __repr__(self):
        """__repr__ method """

        _pipe = "OK" if self.nlpipe else self.nlpipe
        _spa = "OK" if self.nlspa else self.nlspa
        _feat_dict = {k: v[:8] for k, v in self.feature_dict.items()}
        return f"{self.obj_name}(source:{self.source}, {_feat_dict}, pipe/spacy:{_pipe}/{_spa}"

    def __str__(self):
        """__str__ method """

        return self.__repr__()


# def base_from_text(text: str, source, Object, nlpipe=None, nlspa=None):
#     """ """

#     try:
#         return Object(text, source=source, nlpipe=nlpipe, nlspa=nlspa)
#     except Exception as e:
#         return e.__str__()


# def base_from_file(file_path: str, source, Object, nlpipe=None, nlspa=None):
#     """read a file and return  object """

#     try:
#         with open(source, "r") as f:
#             text = f.read()
#     except Exception as e:
#         return e.__str__()

#     return Object(text, source=source, nlpipe=nlpipe, nlspa=nlspa)


# def base_from_url(file_path: str, source, Object, nlpipe=None, nlspa=None):
#     """read a file and return  object """

#     text = requests.get(source)

#     return Object(text, source=source, nlpipe=nlpipe, nlspa=nlspa)
