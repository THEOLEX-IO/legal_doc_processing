"""This module implements NLP methods to handle legal documentation. From text cleaning to information extraction, it centralizes main functionalities that simplify the work for text mining for this category of documents"""
import nltk

nltk.download("stopwords")
# nltk.download("popular")

from legal_doc_processing.legal_doc import LegalDoc, read_LegalDoc

from legal_doc_processing.press_release import PressRelease, read_PressRelease
from legal_doc_processing.press_release.utils import (
    load_press_release_files,
    load_press_release_text_list,
)
from legal_doc_processing.utils import boot, get_pipeline


if __name__ == "__main__":

    nlpipe = get_pipeline()

    # press rel
    press_rel_list = load_press_release_text_list()

    # 1st one
    pr = PressRelease(press_rel_list[0], nlpipe=nlpipe)
    pr.predict("all")

    # all one
    pr_list = [PressRelease(f, nlpipe=nlpipe) for f in press_rel_list]
    _ = [pr.predict("all") for pr in pr_list]
    pr_list