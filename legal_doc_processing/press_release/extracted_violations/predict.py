from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all

from legal_doc_processing.press_release.extracted_violations.clean import (
    _clean_str_to_str,
    _clean_list_to_list,
    clean_ans,
)


from legal_doc_processing.press_release.extracted_violations.questions import (
    _question_helper,
    _question_selector,
    _question_lister,
)


def predict_extracted_violations(
    data: dict,
    h1_len_threshold: int = 15,
    content_n_sents_threshold: int = 5,
    threshold: float = 0.25,
) -> list:
    """ """

    # sents
    h1 = [data.h1] if len(data.h1) > h1_len_threshold else [""]
    sent_list = h1 + data.content_sents[:content_n_sents_threshold]
    sent_list = [i.replace("\n", "").strip() for i in sent_list if i]

    # filter
    keys_list = [
        "accus",
        "charg",
        "violat",
        "judgement",
        "ordere",
        "settle",
        "impose",
        "pay",
        "suit",
        "allege",
    ]
    filter_sents = lambda sent: any([(key in sent.lower()) for key in keys_list])
    sents_ok = [(i, j) for i, j in enumerate(sent_list) if filter_sents(j)]

    # quest
    ans_list = list()
    for i, sent in sents_ok:
        key_list = _question_helper(sent)
        if key_list:
            quest_pairs = _question_lister(key_list)
            ans_list.extend(ask_all(sent, quest_pairs, sent=sent, nlpipe=data.nlpipe))

    if not ans_list:
        return [("", 1)]

    # TODO
    # clean
    # for exem FCPA remplace  "Foreign Corrupt Practices Act"
    # clean len() > 12

    # merged_ans
    answer_label = "answer"
    merged_ans = merge_ans(ans_list, label=answer_label)

    # TODO
    # filter
    # delete no orgs or person in the result
    # delete all of the defendants form response

    # filter by threshold
    flatten_ans = [(i[answer_label], i["cum_score"]) for i in merged_ans]
    last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

    return last_ans


# def predict_extracted_violations(obj: dict, threshold=0.4, n_sents: int = 5) -> list:
#     """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

#     # pers_org_entities_list
#     pers_org_all = obj["pers_org_all"] + _u(_clean_list_to_list(obj["pers_org_all"]))
#     pers_org_all = _u(pers_org_all)

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
#     consitant_ans = [i for i in merged_ans if i[answer_label] not in pers_org_all]

#     # filter by threshold
#     flatten_ans = [(i[answer_label], i["cum_score"]) for i in consitant_ans]
#     last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

#     return [(i.lower(), j) for i, j in last_ans]
