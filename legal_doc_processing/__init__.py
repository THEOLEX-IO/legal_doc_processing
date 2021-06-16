"""This module implements NLP methods to handle legal documentation. From text cleaning to information extraction, it centralizes main functionalities that simplify the work for text mining for this category of documents"""
import nltk

# nltk.download("stopwords")
# nltk.download("punkt")
# nltk.download("popular")

import legal_doc_processing.ld as ld
import legal_doc_processing.pr as pr

from legal_doc_processing.utils import boot, get_pipeline
