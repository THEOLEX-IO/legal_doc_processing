"""This module implements NLP methods to handle legal documentation. From text cleaning to information extraction, it centralizes main functionalities that simplify the work for text mining for this category of documents"""

import os
import logging

from params import GeneralParams as Params
from params import setBasicConfig

# pre set the logger
setBasicConfig(os.getenv("SERVICE_NAME", "LEGAL_DOC_PROCESSING"), Params)
logger = logging.getLogger()
logger.info("called")


# from legal_doc_processing._legal_doc import _LegalDoc as legal_doc
from legal_doc_processing.press_release.press_release import (
    _PressRelease as press_release,
)

# from legal_doc_processing._decision import _Decision as decision
