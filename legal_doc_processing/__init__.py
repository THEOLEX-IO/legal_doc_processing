"""This module implements NLP methods to handle legal documentation. From text cleaning to information extraction, it centralizes main functionalities that simplify the work for text mining for this category of documents"""
import nltk

nltk.download("stopwords")
# nltk.download("popular")

from legal_doc_processing.legal_doc import LegalDoc, read_LegalDoc
from legal_doc_processing.legal_doc.utils import (
    load_legal_doc_files,
    load_legal_doc_text_list,
)

from legal_doc_processing.press_release import PressRelease, read_PressRelease
from legal_doc_processing.press_release.utils import (
    load_press_release_files,
    load_press_release_text_list,
)

from legal_doc_processing.utils import boot, get_pipeline
