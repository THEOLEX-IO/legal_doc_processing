import os

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_spacy,
    _if_not_pipe,
    get_spacy,
    _ask,
)


# from spacy.lang.en import English


nlp = nlspa = get_spacy()
nlp.add_pipe("sentencizer")

doc = nlp(
    "This is a\n sentence. This is another sentence. I work at Global Inc. and it is so fun!"
)


ll = [i for i in doc.sents]

# # Construction via add_pipe
# nlp = nlspa = get_spacy()
# sentencizer = nlp.add_pipe("sentencizer")

# # Construction from class
# from spacy.pipeline import Sentencizer

# sentencizer = Sentencizer()