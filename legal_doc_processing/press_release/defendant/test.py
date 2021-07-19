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

# def f(data):
#     # sents
#     if len(data.h1) > 20:
#         h1 = data.h1
#     abstract_list = data.content_sents[:5]
#     sent_list = [h1] + abstract_list
#     # clean
#     sent_list = [i.replace("\n", "") for i in sent_list if i]

#     # quest
#     ans_list = list()
#     for sent in sent_list:
#         key_list = _question_helper(sent)
#         quest_pairs = _u([_question_selector(key) for key in key_list])
#         ans_list.extend(ask_all(sent, quest_pairs, sent=sent, nlpipe=data.nlpipe))

#     return ans_list, quest_pairs


# paris = df.data.apply(f)