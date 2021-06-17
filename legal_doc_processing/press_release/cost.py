import os
import copy

import pandas as pd


from legal_doc_processing.utils import (
    _if_not_pipe,
    _if_not_spacy,
    get_spacy,
    _ask,
    get_label_,
)


def _get_entities_money(struct_doc: dict, n_paragraphs: int = 2, nlspa=None) -> list:
    """get entities MONEY from h1 and sub_article """

    nlspa = _if_not_spacy(nlspa)

    # sub article
    sub_article = "\n".join(struct_doc["article"].split("\n")[:n_paragraphs])

    # all pers all orgs from spacy entities
    all_money = get_label_(struct_doc["h1"], "MONEY", nlspa) + get_label_(
        sub_article, "MONEY", nlspa
    )
    all_money = list(set(all_money))

    # clean
    all_init_money = _cast_as_int(all_money)

    all_init_money = list(set(all_init_money))

    return all_init_money


def _cast_as_int(cleaned_ans):
    """transform a list of numbers in ints """

    MULTI = [("thousand", 1000), ("million", 1_000_000), ("billion", 1_000_000_000)]

    cleaned_ans = [i.lower().strip() for i in cleaned_ans]

    # delette € or $
    cleaned_ans = [
        i.replace("$", "").replace("€", "").replace("£", "") for i in cleaned_ans
    ]

    # thousands as thousand
    cleaned_ans = [
        i.replace("thousands", "thousand")
        .replace("millions", "million")
        .replace("billions", "billion")
        .replace("hundreds", "hundred")
        for i in cleaned_ans
    ]

    cleaned_ans_multi = list()
    for ans in cleaned_ans:
        multi = ""
        for k, _ in MULTI:
            if k in ans:
                multi = k
                break

        cleaned_ans_multi.append((ans, multi))

    cleaned_ans_multi_2 = list()
    for numb, multi in cleaned_ans_multi:
        if not multi:
            # dump centimies
            numb = numb.split(".")[0]
            # easy, jsute keep the numbers
            numb = "".join([c for c in list(numb) if c.isnumeric()])
            numb = int(numb)
        else:
            # clean the numb: 1, 12 -> 1.22
            numb = numb.split(multi)[0].replace(",", ".").strip()

            # find last numberic and clean : a total of 3.12 -> 3.12
            cands_list = [i for i in numb.split(" ") if i[0].isnumeric()]
            cand = cands_list[-1].strip()

            # specific a 'total of for 3 000' ->  '3000'
            try:
                if cands_list[-2].strip()[0].isnumeric():
                    cand = str(cands_list[-2].strip()) + str(cand)
            except Exception as e:
                pass

            numb = float(cand.strip())

            # make 1.3 million -> 1.3 * 1 000 000 = 1 300 000
            for mm, k in MULTI:
                if mm == multi:
                    numb *= k

        cleaned_ans_multi_2.append(int(numb))

    return cleaned_ans_multi_2


def predict_cost(struct_doc: list, nlpipe=None, nlspa=None):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe, spa
    nlpipe = _if_not_pipe(nlpipe)
    nlspa = _if_not_spacy(nlspa)

    # items
    h1 = struct_doc["h1"]
    sub_article = "\n".join(struct_doc["article"].split("\n")[:2])

    # get_label_ h1
    money_h1 = get_label_(h1, "MONEY", nlspa)
    # print(f"money_h1 is {money_h1}")
    money_h1_clean = list(set(_cast_as_int(money_h1)))
    # print(f"money_h1_clean is {money_h1_clean}")

    # cost in h1
    if len(money_h1_clean) == 1:
        return str(money_h1_clean[0])

    if len(money_h1_clean) > 1:
        return str(-2)

    # get_label article

    money_sub_article = get_label_(sub_article, "MONEY", nlspa)
    # print(f"money_sub_article is {money_sub_article}")
    money_sub_article_clean = list(set(_cast_as_int(money_sub_article)))
    # print(f"money_sub_article_clean is {money_sub_article_clean}")

    # cost in article
    if len(money_sub_article_clean) == 1:
        return [(str(money_sub_article_clean[0]), 1)]
    elif len(money_sub_article_clean) > 1:
        return [(str(max(money_sub_article_clean)), 1)]
    else:
        return str(-1)

    return str(-3)


#     return resp
if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import get_pipeline, get_spacy, get_label_
    from legal_doc_processing.press_release.loader import press_release_X_y
    from legal_doc_processing.press_release.structure import structure_press_release

    # laod
    nlpipe = get_pipeline()
    nlspa = get_spacy()

    # structured_press_release_r
    df = press_release_X_y(features="cost")
    df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

    # one
    one = df.iloc[0, :]
    # one features
    cost = one.cost
    one_struct = struct_doc = one.structured_txt
    one_h1 = one_struct["h1"]
    one_article = one_struct["article"]
    sub_one_article = "\n".join(one_article.split("\n")[:2])

    # # ents
    # money_h1 = get_label_(one_h1, "MONEY", nlspa)
    # money_article = get_label_(sub_one_article, "MONEY", nlspa)

    # # 1 to len(df)
    # print(f" {'y'.rjust(30)} -->  {'pred'} \n")
    # print(160 * "-")
    # for i in range(0, len(df)):
    #     cost = df.cost.iloc[i]
    #     i_text = df.txt.iloc[i]
    #     i_struct = df["structured_txt"].iloc[i]

    #     i_h1 = i_struct["h1"]
    #     i_article = i_struct["article"]
    #     sub_i_article = "\n".join(i_article.split("\n")[:2])
    #     pred_ans = predict_cost(i_struct, nlspa=nlspa, nlpipe=nlpipe)
    #     print(f" {str(cost).rjust(30)} --> pred : {pred_ans}")
