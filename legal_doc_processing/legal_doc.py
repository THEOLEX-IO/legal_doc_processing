import os


class LegalDoc:
    """main legal doc class """

    def __init__(self, file_path: str):
        """init method of the LegalDoc
        pos args :
            file_path (str) : the complete file path of the txt document to read
        opt args :
            -
        raise :
            -
        return :
            a LegalDoc object"""

        self.file_path = file_path

        with open(file_path, "r") as f:
            self.raw_text = f.read()

        # features
        self.case = None
        self.defendant = None

    def clean(self) -> None:
        """clean the text """

        return None

    def predict_case(self) -> str:
        """predict case, update self.case attr and return the value"""

        self.case = "None"
        return self.case

    def predict_defendant(self) -> str:
        """predict defendant, update self.defendant attr and return the value"""

        self.defendant = "None"
        return self.defendant

    def predict_all(self) -> dict:
        """perform various prediction, udate each attr and return a dict off attrs:value """

        pred = {}
        pred["case"] = self.predict_case()
        pred["defendant"] = self.predict_defendant()

        return pred