from legal_doc_processing import logger
from legal_doc_processing._base import (
    Base,
)

from legal_doc_processing.legal_doc.utils import legal_doc_X_y as load_X_y


class LegalDoc(Base):
    """main LegalDoc class """

    def __init__(
        self,
        text: str,
        source: str = None,
        nlpipe=None,
        nlspa=None,
        n_lines: int = 6,
    ):

        Base.__init__(
            self,
            text=text,
            obj_name="LegalDoc",
            source=source,
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


# def from_file(file_path, source, nlpipe=None, nlspa=None):
#     return base_from_file(file_path, source, LegalDoc, nlpipe=nlpipe, nlspa=nlspa)


# def from_text(txt, source, nlpipe=None, nlspa=None):
#     return base_from_text(txt, source, LegalDoc, nlpipe=nlpipe, nlspa=nlspa)


# def from_url(txt, source, nlpipe=None, nlspa=None):
#     return base_from_url(txt, source, LegalDoc, nlpipe=nlpipe, nlspa=nlspa)


class _LegalDoc:
    LegalDoc = LegalDoc
    load_X_y = load_X_y
