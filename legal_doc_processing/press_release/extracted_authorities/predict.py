import os

from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.press_release.utils import product_juridiction_pairs

from legal_doc_processing.press_release.extracted_authorities.clean import _filter_jur


def predict_extracted_authorities(obj: dict) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe, spa
    nlspa = obj["nlspa"]

    # choose the item
    h1, abstract = obj["h1"], obj["abstract"]

    # both h1 and abstract
    h1 = h1.strip()
    h1 = h1 if h1[-1] != "\n" else h1[:-1]
    h1 = h1 if h1[-1] in [".", ". "] else h1 + ". "
    text = h1 + abstract

    # token filter h1
    tok_h1 = [i.text.lower() for i in nlspa(h1)]
    jur_h1 = [_filter_jur(i) for i in tok_h1]
    jur_h1_clean = _u([i for i in jur_h1 if i])

    # juri h1
    if len(jur_h1_clean) >= 1:
        return [(i, 100) for i in jur_h1_clean]

    # token filter abstract
    tok_abstract = [i.text.lower() for i in nlspa(abstract)]
    jur_abstract = [_filter_jur(i) for i in tok_abstract]
    jur_abstract_clean = _u([i for i in jur_abstract if i])

    # juri abstract
    if len(jur_abstract_clean) >= 1:
        return [(i, 1) for i in jur_abstract_clean]

    return [(str(-3), -1)]


# if __name__ == "__main__":

#     # import
#     import time
#     from legal_doc_processing.utils import get_pipeline, get_spacy
#     from legal_doc_processing.press_release.utils import press_release_X_y
#     from legal_doc_processing.press_release.press_release import PressRelease

#     # laod
#     nlpipe = get_pipeline()
#     nlspa = get_spacy()
#     nlspa.add_pipe("sentencizer")

#     # structured_press_release_r
#     df = press_release_X_y(features="defendant")
#     df = df.iloc[:7, :]
#     df["obj"] = [PressRelease(i, nlpipe=nlpipe, nlspa=nlspa) for i in df.txt.values]

#     # one
#     one = df.iloc[0, :]
#     self = obj = one_obj = one.obj
# #     one_struct = struct_doc = one.structured_txt
# #     one_h1 = one_struct["h1"]
# #     one_article = one_struct["article"]
# #     sub_one_article = "\n".join(one_article.split("\n")[:2])
# #     # pred_h1  ⁼ predict_juridiction(one_h1)
# #     # pred_abstract  ⁼ predict_juridiction(one_h1)
# #     pred = predict_extracted_authorities(one_struct, nlpipe=nlpipe, nlspa=nlspa)

# #     # # 1 to len(df)
# #     # print(f" {'y'.rjust(30)} -->  {'pred'} \n")
# #     # print(160 * "-")
# #     # for i in range(0, len(df)):
# #     #     juridiction = df.juridiction.iloc[i]
# #     #     i_text = df.txt.iloc[i]
# #     #     i_struct = df["structured_txt"].iloc[i]
# #     #     pred_ans = predict_juridiction(i_struct, nlspa=nlspa, nlpipe=nlpipe)
# #     #     print(f" {str(juridiction).rjust(30)} --> pred : {pred_ans}")
