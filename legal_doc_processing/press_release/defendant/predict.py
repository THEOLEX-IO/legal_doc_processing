from legal_doc_processing.press_release.country_of_violation.predict import clean_answer
from legal_doc_processing import logger
from collections import Counter


from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all, cosine_similarity

from legal_doc_processing.press_release.defendant.clean import (
    _sub_you_shall_not_pass,
    clean_ans,
)


def predict_defendant(data: dict) -> list:
    """ """

    return [("-- DUMMY --", 1)]

    
# def predict_defendant(obj: dict, threshold: float = 0.4, n_sents: int = 3) -> list:
#     """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

#     # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
#     nlpipe = obj["nlpipe"]

#     # pers_org_entities_list
#     pers_org_all = obj["pers_org_all"] + _u(_sub_you_shall_not_pass(obj["pers_org_all"]))
#     pers_org_all = _u(pers_org_all)

#     # judge
#     judge_list = [i.strip().lower() for i in obj["feature_dict"]["judge"].split(",")]

#     # items
#     h1, abstract = obj["h1"], obj["abstract"]
#     abstract_sents = obj["abstract_sents"][:n_sents]
#     ans = []

#     # ask medhod
#     for key_h1 in _question_helper(h1):
#         quest_pairs = _u(_question_selector(key_h1))
#         ans.extend(ask_all(h1, quest_pairs, nlpipe=nlpipe))

#     for sent in abstract_sents:
#         key_list = _question_helper(sent)
#         for key in key_list:
#             quest_pairs = _u(_question_selector(key))
#             ans.extend(ask_all(sent, quest_pairs, nlpipe=nlpipe))

#     # clean ans
#     cleaned_ans = clean_ans(ans)
#     answer_label = "new_answer"
#     if not len(cleaned_ans):
#         cleaned_ans = [{answer_label: "--None--", "score": -1}]

#     # merge ans
#     merged_ans = merge_ans(cleaned_ans, label=answer_label)

#     # filert by spacy entities
#     consitant_ans = [i for i in merged_ans if i[answer_label] in pers_org_all]
#     # exclude judge
#     consitant_ans = [
#         i for i in consitant_ans if (i[answer_label].strip().lower() not in judge_list)
#     ]

#     # filter by threshold
#     flatten_ans = [(i[answer_label], i["cum_score"]) for i in consitant_ans]
#     last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

#     return last_ans
