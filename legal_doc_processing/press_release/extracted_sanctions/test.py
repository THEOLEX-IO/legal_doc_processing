from legal_doc_processing import logger

from legal_doc_processing.utils import get_spacy, get_pipeline, ask_all
from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import merge_ans, ask_all, cosine_similarity

from legal_doc_processing.press_release.press_release import (
    PressRelease,
    press_release_df,
)

from legal_doc_processing.press_release.extracted_sanctions.questions import (
    _question_helper,
    _question_selector,
    _question_lister,
)

from legal_doc_processing.press_release.extracted_sanctions.predict import (
    predict_extracted_sanctions,
)

# init
nlpsa = get_spacy()
nlpipe = get_pipeline()

# df
df = press_release_df(
    juridiction="",
    sample=0.25,
)

# data
df["data"] = df.pr.apply(lambda i: i.data)

# args
h1_len_threshold = 15
content_n_sents_threshold = 6
threshold = 0.25

# preds
data_list = df.data[:50].values
pred_list = [predict_extracted_sanctions(data) for data in data_list]
for pred in pred_list:
    input(pred)