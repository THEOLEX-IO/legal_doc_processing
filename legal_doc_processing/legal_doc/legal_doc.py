import os

from legal_doc_processing.base.base import Base, base_from_file, base_from_text
from legal_doc_processing.legal_doc.structure import structure_legal_doc
from legal_doc_processing.legal_doc.information_extraction import *


class LegalDoc(Base):
    """main LegalDoc class """

    def __init__(
        self,
        text: str,
        file_path: str = None,
        nlpipe=None,
        nlspa=None,
        n_lines: int = 30,
    ):

        Base.__init__(
            self,
            text=text,
            obj_name="LegalDoc",
            doctype="order",
            structure_method=structure_legal_doc,
            predict_code_law_violation=predict_code_law_violation,
            predict_country_of_violation=predict_country_of_violation,
            predict_currency=predict_currency,
            predict_decision_date=predict_decision_date,
            predict_defendant=predict_defendant,
            predict_extracted_authorities=predict_extracted_authorities,
            predict_extracted_violations=predict_extracted_violations,
            predict_folder=predict_folder,
            predict_judge=str.lower,
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
        self.h1 = self.struct_text["header"]
        self.first_page = self.struct_text["pages"][0]
        if len(self.struct_text["pages"]) > 1:
            self.first_2_pages = (
                self.struct_text["pages"][0] + self.struct_text["pages"][1]
            )
        else:
            self.first_2_pages = self.struct_text["pages"][0]
        self.abstract = self.first_2_pages

        # set all
        self.set_all()


def from_file(file_path, nlpipe=None, nlspa=None):
    return base_from_file(file_path, LegalDoc, nlpipe=nlpipe, nlspa=nlspa)


def from_text(txt, nlpipe=None, nlspa=None):
    return base_from_text(txt, LegalDoc, nlpipe=nlpipe, nlspa=nlspa)


if __name__ == "__main__":

    # import
    import time
    from legal_doc_processing.utils import get_pipeline, get_spacy
    from legal_doc_processing.press_release.loader import press_release_X_y

    # load
    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # legal_doc df AND  OBj
    df = press_release_X_y()
    df = df.iloc[:7, :]
    df["obj"] = df.txt.apply(lambda i: LegalDoc(i, nlpipe=nlpipe, nlspa=nlspa))

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["preds"] = df.obj.apply(lambda i: i.predict_all())
    t = time.time() - t

    #     # labels
    #     preds_labels = list(df.preds.iloc[0].keys())
    #     for k in preds_labels:
    #         df["pred_" + k] = df.preds.apply(lambda i: i[k])

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ob = obj = self = one.obj
