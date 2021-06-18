import os
import copy

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_pipe,
    _if_not_spacy,
    _ask,
    get_pers,
    get_orgs,
    get_pipeline,
)

from legal_doc_processing.information_extraction.utils import merge_ans, ask_all

from legal_doc_processing.press_release.utils import (
    product_juridic_form,
    get_entities_pers_orgs,
)

from legal_doc_processing.press_release.defendant_clean import (
    _sub_you_shall_not_pass,
    clean_ans,
)


quest_pairs = [
    ("Who is charged?", "ask_who_charged"),
    ("Who is the against?", "ask_who_against"),
    ("Who is the victim?", "ask_who_victim"),
    ("Who is the defendant?", "ask_who_defendant"),
    ("Who has violated?", "ask_who_violated"),
    ("Who has to pay?", "ask_who_pay"),
    ("Who is accused?", "ask_who_accused"),
]


def predict_defendant(
    struct_doc: list,
    nlpipe=None,
    pers_org_entities_list=None,
    threshold=0.4,
):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
    # win lots of time if the method is used in a loop with 100 predictions
    nlpipe = _if_not_pipe(nlpipe)

    # pers_org_entities_list
    # we will use this one later to make a filter at the end
    if not pers_org_entities_list:
        pers_org_entities_list = get_entities_pers_orgs(struct_doc)
    pers_org_entities_list = _sub_you_shall_not_pass(pers_org_entities_list)

    # items
    # we will work on h1 and / or article but just 2 or 3 1st paragraphs
    h1 = struct_doc["h1"]
    sub_article = "\n".join(struct_doc["article"].split("\n")[:2])

    # ask medhod
    # here are the question answering and the true prediction built
    ans_h1 = ask_all(h1, quest_pairs, nlpipe)
    ans_article = ask_all(sub_article, quest_pairs, nlpipe)
    ans = ans_h1 + ans_article

    # clean ans
    # ans is a list of dict, each dict has keys such as answer, score etc
    # for each answer we will clean this answer and create a new_answer more accurate
    cleaned_ans = clean_ans(ans)

    # merge ans
    # based on new_answer we will make a groupby adding the scores for each new ans in a cumulative score
    # example [{new_ans : hello, score:0.3},{new_ans : hello, score:0.3}, ]
    # will become  [{new_ans : hello, score:0.6},]
    merged_ans = merge_ans(cleaned_ans, label="new_answer")

    # filert by spacy entities
    # we are sure that a personn or an org is NOT a violation so
    # if a prediction is in pers_org_entities_list, plz drop it
    consitant_ans = [i for i in merged_ans if i["new_answer"] in pers_org_entities_list]

    # filter by threshold
    # we need to filter the score above which we consider that no a signe score but a
    # cumulative score (much more strong, accurante and solid) will be droped
    flatten_ans = [(i["new_answer"], i["cum_score"]) for i in consitant_ans]
    last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

    return last_ans


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import get_pipeline, get_spacy, get_orgs, get_pers
    from legal_doc_processing.press_release.loader import press_release_X_y
    from legal_doc_processing.press_release.structure import structure_press_release

    # laod
    nlpipe = get_pipeline()
    # nlspa = get_spacy()
    pers_org_entities_list = None

    # structured_press_release_r
    df = press_release_X_y(features="defendant")
    df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

    # one
    one = df.iloc[0, :]
    one_defendant = one.defendant
    one_struct = struct_doc = one.structured_txt
    one_h1 = one_struct["h1"]
    one_article = one_struct["article"]
    sub_one_article = "\n".join(one_article.split("\n")[:2])

    # pred one
    pred = predict_defendant(one_struct, nlpipe)

    # ents
    # org_h1 = get_label_(one_h1)
    # org_article = get_label_(sub_one_article)
    # pers_h1 = get_pers(one_h1)
    # pers_article = get_pers(sub_one_article)

    # print(f" {'y'.rjust(80)} -->  {'pred'} \n")
    # print(160 * "-")
    # print(f" {defendant.rjust(80)} -->  {pred[:60]} \n")

    # # 1 to len(df)
    # print(f" {'y'.rjust(60)} -->  {'pred'} \n")
    # print(160 * "-")
    # for i in range(0, len(df)):
    #     defendant = df.defendant.iloc[i]
    #     i_text = df.txt.iloc[i]
    #     i_struct = df["structured_txt"].iloc[i]
    #     pred = predict_defendant(i_struct, nlpipe)
    #     print(f" {defendant.rjust(60)} -->  {pred[:100]} \n")