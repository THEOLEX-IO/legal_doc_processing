from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all
from legal_doc_processing.press_release.penalty_details.clean import clean_ans


def predict_penalty_details(data: dict) -> list:
    """ """

    sanctions = data._feature_dict["_extracted_sanctions"]

    sanctions = [(i, j) for i, j in sanctions if "$" in i]

    return sanctions


# def predict_penalty_details(obj: dict, threshold=0.4, n_sents: int = 5) -> list:
#     """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

#     # extracted_violations
#     extracted_violations = obj["feature_dict"]["extracted_violations"].lower().split(",")
#     # extracted_violations = [i.lower().strip() for i in extracted_violations]

#     # items
#     h1, abstract = obj["h1"], obj["abstract"]
#     abstract_sents = obj["abstract_sents"][:n_sents]
#     ans = []

#     # ask medhod h1
#     for key_h1 in _question_helper(h1):
#         # print(f"key_h1 : {key_h1} ")
#         quest_pairs = _u(_question_selector(key_h1))
#         # print(f"quest_pairs : {quest_pairs} ")
#         ans.extend(ask_all(h1, quest_pairs, nlpipe=obj["nlpipe"]))

#     # ask medhod abstract_sents
#     for sent in abstract_sents:
#         key_list = _question_helper(sent)
#         for key in key_list:
#             # print(key)
#             quest_pairs = _u(_question_selector(key))
#             # print(quest_pairs)
#             ans.extend(ask_all(sent, quest_pairs, nlpipe=obj["nlpipe"]))

#     # clean ans
#     cleaned_ans = clean_ans(ans)
#     answer_label = "new_answer"
#     if not len(cleaned_ans):
#         cleaned_ans = [{answer_label: "--None--", "score": -1}]

#     # merge ans
#     merged_ans = merge_ans(cleaned_ans, label=answer_label)

#     # filert by spacy entities
#     consitant_ans = [
#         i for i in merged_ans if i[answer_label] if i not in extracted_violations
#     ]

#     # filter by threshold
#     flatten_ans = [(i[answer_label], i["cum_score"]) for i in consitant_ans]
#     last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

#     return [(i.lower(), j) for i, j in last_ans]
