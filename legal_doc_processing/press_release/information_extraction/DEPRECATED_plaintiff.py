# import os

# import pandas as pd

# from legal_doc_processing.utils import _if_not_pipe, _ask, _if_not_spacy


# def predict_plaintiff(obj: dict) -> list:
#     """ """

#     return [(-1, -1)]


# # def _ask_all(txt, nlpipe) -> list:
# #     """asl all questions and return a list of dict """

# #     # pipe
# #     nlpipe = _if_not_pipe(nlpipe)

# #     # ans
# #     ans = []

# #     # question, funct
# #     quest_pairs = [
# #         ("Who make the charges?", "ask_who_charges"),
# #         ("Who ask something?", "ask_who_ask"),
# #         ("Who has order something?", "ask_who_has_order"),
# #         ("Who enter judgement against someone", "ask_who_enter_judgement"),
# #     ]

# #     # loop
# #     for quest, label in quest_pairs:
# #         ds = _ask(txt=txt, quest=quest, nlpipe=nlpipe)
# #         _ = [d.update({"question": label}) for d in ds]
# #         ans.extend(ds)

# #     # sort
# #     ans = sorted(ans, key=lambda i: i["score"], reverse=True)

# #     # clean
# #     ans = [i for i in ans if (i["answer"].lower() != "defendants")]

# #     return ans


# # def _clean_ans(ans, threshold=0.5):
# #     """ """

# #     # build dataframe
# #     df = pd.DataFrame(ans)
# #     df = df.loc[:, ["score", "answer"]]

# #     # group by ans and make cumutavie score of accuracy
# #     ll = [
# #         {"answer": k, "cum_score": v.score.sum()}
# #         for k, v in df.groupby("answer")
# #         if v.score.sum() > threshold
# #     ]
# #     ll = sorted(ll, key=lambda i: i["cum_score"], reverse=True)

# #     return ll


# # def predict_plaintiff(struct_doc: list, nlpipe=None, nlspa=None):
# #     """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

# #     # pipe, spa
# #     nlpipe = _if_not_pipe(nlpipe)
# #     nlspa = _if_not_spacy(nlspa)

# #     # choose the item
# #     h1 = struct_doc["h1"]
# #     sub_article = "\n".join(struct_doc["article"].split("\n")[:2])

# #     # # ask all and get all possible response
# #     # ans = _ask_all(h1, nlpipe)

# #     # # group by ans, make cumulative sum of accuracy for eash ans and filter best ones
# #     # ll = _clean_ans(ans)

# #     # # reponse
# #     # resp = ", ".join([i["answer"] for i in ll])

# #     # return resp

# #     return [("-- None --", -1)]


# # if __name__ == "__main__":

# #     # import
# #     from legal_doc_processing.utils import *
# #     from legal_doc_processing.press_release.utils import *
# #     from legal_doc_processing.press_release.loader import press_release_X_y
# #     from legal_doc_processing.press_release.structure import structure_press_release

# #     # pipe
# #     nlpipe = get_pipeline()
# #     nlspa = get_spacy()

# #     # structured_press_release_r
# #     df = press_release_X_y()
# #     df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

# #     # one
# #     one = df.iloc[0, :]
# #     one_struct = struct_doc = one.structured_txt
# #     one_h1 = one_struct["h1"]
# #     one_article = one_struct["article"]
# #     sub_one_article = "\n".join(one_article.split("\n")[:2])
# #     # pred_h1  ⁼ predict_juridiction(one_h1)
# #     # pred_sub_article  ⁼ predict_juridiction(one_h1)
# #     pred = predict_plaintiff(one_struct, nlpipe=nlpipe, nlspa=nlspa)