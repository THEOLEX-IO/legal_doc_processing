from legal_doc_processing import logger

from legal_doc_processing.utils import get_spacy, get_pipeline, ask_all
from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import merge_ans, ask_all, cosine_similarity


from legal_doc_processing.press_release.press_release import (
    PressRelease,
    press_release_df,
)

from legal_doc_processing.utils import merge_ans, ask_all, cosine_similarity

# from legal_doc_processing.press_release.judge.questions import (
#     _question_helper,
#     _question_selector,
#     _question_lister,
# )
# from legal_doc_processing.press_release.judge.clean import clean_ans_list


# init
nlpsa = get_spacy()
nlpipe = get_pipeline()


# df
df = press_release_df(
    juridiction="",
    sample=0.25,
)


# take one data

df["data"] = df.pr.apply(lambda i: i.data)
data = df.data[0]

# sanity check
assert len(data.content) > 100
assert ("judge" or "attorney") in data.content.lower()


# preds
from legal_doc_processing.press_release.monetary_sanction.predict import (
    predict_monetary_sanction,
)

cost = predict_monetary_sanction(data)
