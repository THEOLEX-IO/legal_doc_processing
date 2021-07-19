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


from legal_doc_processing.press_release.extracted_violations.predict import (
    predict_extracted_violations,
)


h1_len_threshold = 15
content_n_sents_threshold = 5
threshold = 0.25


data_list = df.data[20:50].values


def_list = [predict_extracted_violations(data) for data in data_list]
for defs in def_list:
    print(defs)
    input()