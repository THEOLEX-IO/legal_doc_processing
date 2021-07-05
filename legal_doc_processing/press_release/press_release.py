from legal_doc_processing import logger
from legal_doc_processing.base.base import Base, base_from_file, base_from_text
from legal_doc_processing.press_release.structure import structure_press_release
from legal_doc_processing.press_release.information_extraction import *


class PressRelease(Base):
    """main press release doc class """

    def __init__(
        self,
        text: str,
        file_path: str = None,
        nlpipe=None,
        nlspa=None,
        n_lines: int = 6,
    ):

        Base.__init__(
            self,
            text=text,
            obj_name="PressRelease",
            doctype="press",
            structure_method=structure_press_release,
            predict_code_law_violation=predict_code_law_violation,
            predict_country_of_violation=predict_country_of_violation,
            predict_currency=predict_currency,
            predict_decision_date=predict_decision_date,
            predict_defendant=predict_defendant,
            predict_extracted_authorities=predict_extracted_authorities,
            predict_extracted_violations=predict_extracted_violations,
            predict_folder=predict_folder,
            predict_judge=predict_judge,
            predict_justice_type=predict_justice_type,
            predict_monetary_sanction=predict_monetary_sanction,
            predict_monitor=predict_monitor,
            predict_nature_de_sanction=predict_nature_de_sanction,
            predict_nature_of_violations=predict_nature_of_violations,
            predict_penalty_details=predict_penalty_details,
            predict_reference=predict_reference,
            predict_type=predict_type,
            # predict_sentence=predict_sentence,
            # predict_violation_date=predict_violation_date,
            file_path=file_path,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )

        # specs
        self.h1 = self.struct_text["h1"]
        self.abstract = "\n".join(self.struct_text["article"].split("\n")[:n_lines])

        # set all
        self.set_all()

        # all_text_sents
        self.all_text_sents = [
            i.text
            for i in self.nlspa(self.struct_text["article"]).sents
            if i.text.strip()
        ]


def from_file(file_path, nlpipe=None, nlspa=None):
    return base_from_file(file_path, PressRelease, nlpipe=nlpipe, nlspa=nlspa)


def from_text(txt, nlpipe=None, nlspa=None):
    return base_from_text(txt, PressRelease, nlpipe=nlpipe, nlspa=nlspa)
