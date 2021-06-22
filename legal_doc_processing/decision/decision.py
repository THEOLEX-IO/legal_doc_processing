import os

from legal_doc_processing.legal_doc.legal_doc import LegalDoc
from legal_doc_processing.press_release.press_release import PressRelease
from legal_doc_processing.utils import get_pipeline, get_spacy
from legal_doc_processing.base.base import Base, base_from_file, base_from_text


class Decision(Base):
    def __init__(
        self,
        press_release_text: str,
        legal_doc_text: str,
        press_release_file_path: str = None,
        legal_doc_file_path: str = None,
        nlpipe=None,
        nlspa=None,
    ):

        Base.__init__(
            self,
            text="",
            obj_name="Decision",
            structure_method=str.upper,
            predict_code_law_violation=predict_code_law_violation,
            predict_country_of_violation=predict_country_of_violation,
            predict_currency=predict_currency,
            predict_decision_date=predict_decision_date,
            predict_defendant=predict_defendant,
            predict_extracted_authorities=predict_extracted_authorities,
            predict_id=predict_id,
            predict_juridiction=predict_juridiction,
            predict_monetary_sanction=predict_monetary_sanction,
            predict_nature_of_violations=predict_nature_of_violations,
            predict_plaintiff=predict_plaintiff,
            predict_reference=predict_reference,
            predict_sentence=predict_sentence,
            # predict_violation_date=predict_violation_date,
            file_path="",
            nlpipe=nlpipe,
            nlspa=nlspa,
        )

        self.legal_doc = LegalDoc(
            legal_doc_text,
            file_path=legal_doc_file_path,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )
        self.press_release = PressRelease(
            press_release_text,
            file_path=press_release_file_path,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )

    ######################

    def predict(self, feature) -> str:
        """ """

        if feature == "all":
            return self.predict_all()

        if feature in self.feature_list:
            # try:
            val = self._predict[feature](self.press_release.data, self.legal_doc.data)
            setattr(self, "_" + feature, val)
            return val
            # except:
            #     return "--Error--"
        return "--Unknowned feature--"

    def predict_all(self) -> str:
        """return self.predict("all") """

        for feature in self.feature_list:
            setattr(
                self,
                "_" + feature,
                self._predict[feature](self.press_release.data, self.legal_doc.data),
            )


def from_file(press_release, legal_doc, nlpipe=None, nlspa=None):

    nlpipe = nlpipe if nlpipe else get_pipeline()
    nlspa = nlspa if nlspa else get_spacy()
    try:
        nlspa.add_pipe("sentencizer")
    except Exception as e:
        pass

    press_release_text = ""
    try:
        with open(press_release, "r") as f:
            press_release_text = f.read()
    except Exception as e:
        print(e.__str__())

    legal_doc_text = ""
    try:
        with open(legal_doc, "r") as f:
            legal_doc_text = f.read()
    except Exception as e:
        print(e.__str__())

    if legal_doc_text and press_release_text:
        return Decision(
            press_release_text,
            legal_doc_text,
            press_release_file_path=press_release,
            legal_doc_file_path=legal_doc,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )
    elif legal_doc_text and (not press_release_text):
        return LegalDoc(
            legal_doc_text,
            file_path=legal_doc,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )
    elif (not legal_doc_text) and press_release_text:
        return PressRelease(
            press_release_text,
            file_path=press_release,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )
    else:
        raise NotImplementedError("something went wrong mother fucker :) ")


def from_text(press_release, legal_doc, nlpipe=None, nlspa=None):

    nlpipe = nlpipe if nlpipe else get_pipeline()
    nlspa = nlspa if nlspa else get_spacy()
    try:
        nlspa.add_pipe("sentencizer")
    except Exception as e:
        pass

    if legal_doc and press_release:
        return Decision(
            press_release,
            legal_doc,
            press_release_file_path=press_release,
            legal_doc_file_path=legal_doc,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )
    elif legal_doc and (not press_release):
        return LegalDoc(
            legal_doc,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )
    elif (not legal_doc) and press_release:
        return PressRelease(
            press_release,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )
    else:
        raise NotImplementedError("something went wrong mother fucker :) ")
