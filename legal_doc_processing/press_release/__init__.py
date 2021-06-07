import os


import legal_doc_processing.press_release.information_extraction as ext
import legal_doc_processing.press_release.segmentation as seg
from legal_doc_processing.press_release.utils import (
    load_press_release_files,
    load_press_release_text_list,
)

from legal_doc_processing.utils import get_pipeline
from legal_doc_processing.utils import load_data


class PressRelease:
    """main press release doc class """

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
            a Press Release object"""

        # args as attr
        self.file_path = os.path.dirname(file_path) if file_path else None
        self.file_name = os.path.basename(file_path) if file_path else None
        self.nlpipe = nlpipe if nlpipe else get_pipeline()

        # text and clean
        self.raw_text = text
        self.struct_text = seg.structure_press_release(text)

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
            self.case = None
            return None
        elif feature == "id":
            self.id = ext.predict_id(
                self.struct_text,
            )
            return self.id
        elif feature == "date":
            self.date = ext.predict_date(
                self.struct_text,
            )
            return self.date
        elif feature == "defendant":
            self.defendant = ext.predict_defendant(self.struct_text, self.nlpipe)
            return self.defendant
        elif feature == "plaintiff":
            self.plaintiff = ext.predict_plaintiff(self.struct_text, self.nlpipe)
            return self.plaintiff
        elif feature == "cost":
            self.cost = ext.predict_cost(self.struct_text, self.nlpipe)
            return self.cost
        elif feature == "sentence":
            self.sentence = ext.predict_sentence(self.struct_text, self.nlpipe)
            return self.sentence
        elif feature == "all":
            self.id = ext.predict_id(self.struct_text)
            self.date = ext.predict_date(self.struct_text)
            self.defendant = ext.predict_defendant(self.struct_text, self.nlpipe)
            self.plaintiff = ext.predict_plaintiff(self.struct_text, self.nlpipe)
            self.cost = ext.predict_cost(self.struct_text, self.nlpipe)
            self.sentence = ext.predict_sentence(self.struct_text, self.nlpipe)
            return self.feature_dict
        else:
            raise AttributeError("feature Not Implemented")

    def predict_all(self) -> str:
        """return self.predict("all") """

        return self.predict("all")

    def __repr__(self):
        """__repr__ method """

        return f"PressRelease(path:{self.file_path}, file:{self.file_name}, case:{self.case}, defendant:{self.defendant}, pipe:{'OK' if self.nlpipe else self.nlpipe})"

    def __str__(self):
        """__str__ method """

        return "a LegalDoc Instance"


def read_PressRelease(file_path: str, nlpipe=None):
    """read a file and return a PressRelease object """

    with open(file_path, "r") as f:
        text = f.read()

    return PressRelease(text, file_path=file_path, nlpipe=nlpipe)


if __name__ == "__main__":

    nlpipe = get_pipeline()

    # press rel
    press_rel_list = load_press_release_text_list()

    # 1st one
    press_text_0 = press_rel_list[0]
    pr = PressRelease(press_text_0, nlpipe=nlpipe)
    pred = pr.predict("all")

    # all
    pr_list = [PressRelease(f, nlpipe=nlpipe) for f in press_rel_list]
    preds = [pr.predict("all") for pr in pr_list]
