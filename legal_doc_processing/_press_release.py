from legal_doc_processing import logger
from legal_doc_processing._base import (
    Base,
    base_from_file,
)

from legal_doc_processing.press_release.utils import press_release_X_y


class PressRelease(Base):
    """main press release doc class """

    def __init__(
        self,
        text: str,
        source: str,
        nlpipe=None,
        nlspa=None,
        n_lines: int = 6,
    ):

        Base.__init__(
            self,
            text=text,
            obj_name="PressRelease",
            source=source,
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


# def from_file(file_path, source, nlpipe=None, nlspa=None):
#     return base_from_file(file_path, source, PressRelease, nlpipe=nlpipe, nlspa=nlspa)


# def from_text(txt, source, nlpipe=None, nlspa=None):
#     return base_from_text(txt, source, PressRelease, nlpipe=nlpipe, nlspa=nlspa)


# def from_url(txt, source, nlpipe=None, nlspa=None):
#     return base_from_url(txt, source, PressRelease, nlpipe=nlpipe, nlspa=nlspa)


class _PressRelease:
    PressRelease = PressRelease
    load_X_y = press_release_X_y