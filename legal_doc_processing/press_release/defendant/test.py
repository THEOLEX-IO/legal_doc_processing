from legal_doc_processing import logger

from legal_doc_processing.utils import get_spacy, get_pipeline, ask_all
from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import merge_ans, ask_all, cosine_similarity
from legal_doc_processing.press_release.defendant.clean import (
    _sub_you_shall_not_pass,
    clean_ans,
)

from legal_doc_processing.utils import merge_ans, ask_all, cosine_similarity
from legal_doc_processing.press_release.defendant.questions import (
    _question_helper,
    _question_selector,
    _question_lister,
)

from legal_doc_processing.press_release.press_release import (
    PressRelease,
    press_release_df,
)


# init
nlpsa = get_spacy()
nlpipe = get_pipeline()


# df
df = press_release_df(
    juridiction="",
    sample=0.25,
)

df["data"] = df.pr.apply(lambda i: i.data)


data = df.data[0]

from legal_doc_processing.press_release.defendant.predict import predict_defendant


defs = predict_defendant(data)
