import os


from legal_doc_processing.utils import clean_doc
import legal_doc_processing.information_extraction as infext


class LegalDoc:
    """main legal doc class """

    def __init__(self, text: str):
        """init method of the LegalDoc
        pos args :
            text (str) : the complete text to proceed
        opt args :
            -
        raise :
            -
        return :
            a LegalDoc object"""

        # raw text
        self.file_path = None
        self.raw_text = text
        self.clean_text = None

        # features
        self.case = None
        self.defendant = None

    def clean(self) -> None:
        """clean the text """

        self.clean_text = clean_doc(self.raw_text)

        return self.clean_text

    def predict_case(self) -> str:
        """predict case, update self.case attr and return the value"""

        self.case = infext.get_case(self.clean_text[1])
        return self.case

    def predict_defendant(self) -> str:
        """predict defendant, update self.defendant attr and return the value"""

        self.defendant = "-None-"
        return self.defendant

    def predict_all(self) -> dict:
        """perform various prediction, udate each attr and return a dict off attrs:value """

        pred = {}
        pred["case"] = self.predict_case()
        pred["defendant"] = self.predict_defendant()

        return pred

    def __repr__(self):
        """__repr__ method """

        return "a LegalDoc Instance"

    def __str__(self):
        """__str__ method """

        return "a LegalDoc Instance"


def read_file(file_path: str):
    """read a file and return a LegalDoc object """

    with open(file_path, "r") as f:
        text = f.read()

    ld = LegalDoc(text)
    ld.file_path = file_path

    return ld
