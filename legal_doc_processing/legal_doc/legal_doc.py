import os

from legal_doc_processing.information_extraction.case import get_case
from legal_doc_processing.information_extraction.defendant import get_defendant
from legal_doc_processing.information_extraction.utils import get_pipeline
from legal_doc_processing.segmentation.clean import clean_doc


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

        # text and clean
        self.raw_text = text
        self.clean_pages = clean_doc(text)

        # features
        self.case = None
        self.defendant = None

    def predict_case(self) -> str:
        """predict case, update self.case attr and return the value"""

        self.case = get_case(self.clean_pages[0])

        return self.case

    def predict_defendant(self) -> str:
        """predict defendant, update self.defendant attr and return the value"""

        joined_first_page = ".".join(self.clean_pages[0])
        self.defendant = get_defendant(joined_first_page, self.nlpipe)

        return self.defendant

    def predict_all(self) -> dict:
        """perform various prediction, udate each attr and return a dict off attrs:value """

        pred = {}
        pred["case"] = self.predict_case()
        pred["defendant"] = self.predict_defendant()

        return pred

    def __repr__(self):
        """__repr__ method """

        return f"LegalDoc(path:{self.file_path}, file:{self.file_name}, case:{self.case}, defendant:{self.defendant}, pipe:{'OK' if self.nlpipe else self.nlpipe})"

    def __str__(self):
        """__str__ method """

        return "a LegalDoc Instance"


def read_file(file_path: str, nlpipe=None):
    """read a file and return a LegalDoc object """

    with open(file_path, "r") as f:
        text = f.read()

    ld = LegalDoc(text, file_path=file_path, nlpipe=nlpipe)
    return ld
