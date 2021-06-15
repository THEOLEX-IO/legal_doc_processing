import os

from legal_doc_processing.utils import get_pipeline

import legal_doc_processing.legal_doc.information_extraction as ext
import legal_doc_processing.legal_doc.segmentation.clean as clean
import legal_doc_processing.legal_doc.segmentation.structure as struct
from legal_doc_processing.legal_doc.utils import (
    load_legal_doc_files,
    load_legal_doc_text_list,
)
from legal_doc_processing.utils import load_data


class LegalDoc:
    """main legal doc class """

    def __init__(self, text: str, file_path: str = None, nlpipe=None):
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

        # text and cleanstructure
        self.raw_text = text
        self.clean_pages = clean.clean_doc(text)
        self.structured_text = struct.structure_legal_doc(text)
        self.first_page = []

        for k in range(4):
            try:
                self.first_page.extend(self.clean_pages[k])
            except Exception as e:
                break

        # features
        self.feature_list = [
            "case",
            "id",
            "date",
            "defendant",
            "plaintiff",
            "cost",
            "sentence",
            "violation",
            "juridiction",
        ]

        _ = [setattr(self, k, None) for k in self.feature_list]

    @property
    def feature_dict(self):
        return {k: getattr(self, k) for k in self.feature_list}

    def predict(self, feature) -> str:
        """ """
        if feature == "case":
            self.case = ext.predict_case(
                self.first_page,
            )
            return self.case
        elif feature == "date":
            self.date = ext.predict_date(
                self.first_page,
            )
            return self.date
        elif feature == "defendant":
            self.defendant = ext.predict_defendant(self.first_page, self.nlpipe)
            return self.defendant
        elif feature == "plaintiff":
            self.plaintiff = ext.predict_plaintiff(self.first_page, self.nlpipe)
            return self.plaintiff
        elif feature == "cost":
            self.cost = ext.predict_cost(self.first_page, self.nlpipe)
            return self.cost
        elif feature == "sentence":
            self.sentence = ext.predict_sentence(self.first_page, self.nlpipe)
            return self.sentence
        elif feature == "all":
            self.case = ext.predict_case(self.first_page)
            self.date = ext.predict_date(self.first_page)
            self.defendant = ext.predict_defendant(self.first_page, self.nlpipe)
            self.plaintiff = ext.predict_plaintiff(self.first_page, self.nlpipe)
            self.cost = ext.predict_cost(self.first_page, self.nlpipe)
            self.sentence = ext.predict_sentence(self.first_page, self.nlpipe)
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


def read_LegalDoc(file_path: str, nlpipe=None):
    """read a file and return a LegalDoc object """

    with open(file_path, "r") as f:
        text = f.read()

    return LegalDoc(text, file_path=file_path, nlpipe=nlpipe)


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import get_pipeline, get_spacy, get_orgs, get_pers
    from legal_doc_processing.legal_doc.utils import legal_doc_X_y
    from legal_doc_processing.legal_doc.segmentation.structure import (
        structure_legal_doc,
    )

    # laod
    nlpipe = get_pipeline()
    nlpspa = get_spacy()

    # legal_doc structured
    df = legal_doc_X_y()
    df["obj"] = df.txt.apply(lambda i: LegalDoc(i, nlpipe=nlpipe))

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ld = one.obj
    pred = one_ld.predict_all()
