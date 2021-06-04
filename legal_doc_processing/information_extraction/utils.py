# import re
import pickle

import spacy
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer


def get_pipeline():
    """ build and return a piplein"""

    return pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad",
        tokenizer="distilbert-base-cased",
    )


# DEPRECATED

# def save_pipeline():
#     """init a pipeline and save in a pk """

#     with open("./utils/pipe.pk", "wb") as f:
#         nlpipe = get_pipeline()
#         obj = pickle.dumps(nlpipe)
#         f.write(obj)


# def load_pipeline():
#     """load apickled object """

#     with open("./utils/pipe.pk", "rb") as f:
#         cand = f.read()
#     nlpipe = pickle.loads(cand)

#     return nlpipe
