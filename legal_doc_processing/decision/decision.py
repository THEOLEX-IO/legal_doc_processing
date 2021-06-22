import os
import time

from legal_doc_processing.legal_doc import LegalDoc
from legal_doc_processing.press_release import PressRelease

from legal_doc_processing.utils import merge_ans, ask_all
from legal_doc_processing.utils import (
    get_pipeline,
    get_spacy,
    _if_not_pipe,
    _if_not_spacy,
)


class Decision:
    pass


def from_file():
    pass


def from_text():
    pass