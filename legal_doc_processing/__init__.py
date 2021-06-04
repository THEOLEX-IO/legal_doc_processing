"""This module implements NLP methods to handle legal documentation. From text cleaning to information extraction, it centralizes main functionalities that simplify the work for text mining for this category of documents"""
import nltk

nltk.download("stopwords")
# nltk.download("popular")

from legal_doc_processing.legal_doc import LegalDoc, read_file
from legal_doc_processing.boot import boot