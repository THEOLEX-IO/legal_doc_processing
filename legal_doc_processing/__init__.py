"""This module implements NLP methods to handle legal documentation. From text cleaning to information extraction, it centralizes main functionalities that simplify the work for text mining for this category of documents"""

import os
import logging

from params import GeneralParams as Params
from params import setBasicConfig

# pre set the logger
setBasicConfig(os.getenv("SERVICE_NAME", "LEGAL_DOC_PROCESSING"), Params)
logger = logging.getLogger()
logger.info("called")


import legal_doc_processing.legal_doc as legal_doc
import legal_doc_processing.press_release as press_release
import legal_doc_processing.decision as decision
