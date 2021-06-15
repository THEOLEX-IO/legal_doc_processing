import os

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_pipe,
    _if_not_spacy, get_spacy,
    _ask,
)

from legal_doc.predict_juridiction.utils import product_juridiction_pairs


def _filter_jur(txt, cands:list=None) : 
    """ """

    if not cands : 
        cands = product_juridiction_pairs()

    for k, v in cands.items() : 
        if txt.lower().strip() == k.lower().strip() : 
            return v.upper()

    return ""


def predict_juridiction(struct_doc: list, nlpipe=None, nlpspa=None):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe, spa
    nlpipe = _if_not_pipe(nlpipe)
    nlpspa = _if_not_spacy(nlpspa)

    # choose the item
    h1 = struct_doc["h1"]
    sub_article = "\n".join(struct_doc["article"].split("\n")[:2])

    # token filter h1
    tok_h1 = [i.txt.lower() for i in nlpspa(h1)]
    jur_h1 = [_filter_jur(i) for i in tok_h1]
    jur_h1_clean = [i for i in jur_h1]

    # juri h1
    if len(jur_h1_clean) == 1 : 
        return jur_h1_clean[0]
    if  len(jur_h1_clean) > 1 : 
        return str(-1)


    # token filter sub_article
    tok_sub_article = [i.txt.lower() for i in nlpspa(sub_article)]
    jur_sub_article = [_filter_jur(i) for i in tok_sub_article]
    jur_sub_article_clean = [i for i in jur_sub_article]

    # juri sub_article
    if len(jur_sub_article_clean) == 1 : 
        return jur_sub_article_clean[0]
    if  len(jur_sub_article_clean) > 1 : 
        return str(-2)

    return str(-3)






    # cost in h1
    if len(money_h1_clean) == 1:
        return str(money_h1_clean[0])

    if len(money_h1_clean) > 1:
        return str(-2)



    if "CFTC" in h1 : 
        return "CFTC"


    if "SEC" in h1 : 
        return "SEC"

    if "DOJ" in h1 : 
        return "DOJ"


    # ask all and get all possible response
    ans = _ask_all(txt, nlpipe)

    # group by ans, make cumulative sum of accuracy for eash ans and filter best ones
    ll = _clean_ans(ans)

    # reponse
    resp = ", ".join([i["answer"] for i in ll])

    return resp


if __name__ == "__main__":

    # # import
    # from legal_doc_processing.utils import *
    # from legal_doc_processing.press_release.utils import *
    # from legal_doc_processing.press_release.segmentation.structure import (
    #     structure_press_release,
    # )

    # # pipe
    # nlpipe = get_pipeline()

    # # struct_doc_list
    # press_txt_list = load_press_release_text_list()
    # struct_doc_list = [structure_press_release(i) for i in press_txt_list]

    # # test one
    # struct_doc = struct_doc_list[0]

    # all_ans_h1 = _ask_all(struct_doc["h1"], nlpipe)
    # all_ans_h2 = _ask_all(struct_doc["h2"], nlpipe)
    # all_ans_article = _ask_all(struct_doc["article"], nlpipe)

    # ans = predict_plaintiff(struct_doc, nlpipe)

    # # test others
    # ans_list = [predict_plaintiff(p, nlpipe) for p in struct_doc_list]
    # clean_ans_list = [[d["answer"] for d in ll] for ll in ans_list]
    # clean_ans_list = [", ".join(ll) for ll in clean_ans_list]
