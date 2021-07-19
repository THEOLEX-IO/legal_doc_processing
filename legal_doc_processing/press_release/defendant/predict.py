from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all, cosine_similarity
from legal_doc_processing.press_release.defendant.questions import (
    _question_helper,
    _question_selector,
    _question_lister,
)
from legal_doc_processing.press_release.defendant.clean import (
    _sub_you_shall_not_pass,
    clean_ans,
)


def predict_defendant(
    data: dict,
    h1_len_threshold: int = 15,
    content_n_sents_threshold: int = 5,
    threshold: float = 0.25,
) -> list:
    """ """

    # sents
    h1 = [data.h1] if len(data.h1) > h1_len_threshold else [""]
    sent_list = h1 + data.content_sents[:content_n_sents_threshold]
    sent_list = [i.replace("\n", "") for i in sent_list if i]

    # quest
    ans_list = list()
    for sent in sent_list:
        key_list = _question_helper(sent)
        if quest_pairs:
            quest_pairs = _question_lister(key_list)
            ans_list.extend(ask_all(sent, quest_pairs, sent=sent, nlpipe=data.nlpipe))

    # clean ans
    cleaned_ans = clean_ans(ans_list)
    answer_label = "new_answer"
    if not len(cleaned_ans):
        cleaned_ans = [{answer_label: "", "score": 1}]
        return cleaned_ans

    # merge ans
    merged_ans = merge_ans(cleaned_ans, label=answer_label)

    # filert by spacy entities
    consitant_ans = [i for i in merged_ans if i[answer_label] in data.pers_org_all]

    # exclude judge
    judge_list = [
        i.lower().replace("judge", "").strip()
        for i in data.feature_dict["judge"].split(",")
    ]
    exclude_judge = lambda i: i[answer_label].strip().lower() not in judge_list
    if judge_list:
        consitant_ans = [i for i in consitant_ans if exclude_judge(i)]

    # filter by threshold
    flatten_ans = [(i[answer_label], i["cum_score"]) for i in consitant_ans]
    last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

    return last_ans
