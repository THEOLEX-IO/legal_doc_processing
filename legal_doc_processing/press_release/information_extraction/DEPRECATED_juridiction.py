# from legal_doc_processing.utils import uniquize as _u

# from legal_doc_processing.utils import merge_ans, ask_all

# from legal_doc_processing.press_release.clean.defendant import (
#     _sub_you_shall_not_pass,
#     clean_ans,
# )


# def _question_helper(txt) -> list:
#     """txt"""

#     _txt = txt.lower()
#     res = list()

#     cands = [
#         "impose",
#         "judgment",
#         "order",
#         "settl",
#         "charge",
#         "against",
#         "violate",
#     ]

#     for cand in cands:
#         if cand in _txt:
#             res.append(cand)

#     return res


# def _question_selector(key: str) -> list:
#     """based on a key from _question helper find the list of good question to ask """

#     qs = list()

#     if "impose" in key:  # impose
#         qs.extend(
#             [
#                 ("Who has imposed something?", "who_imposed"),
#                 ("Who ask something?", "who_imposed"),
#                 ("Who imposed something?", "who_imposed"),
#                 # ("Who  imposed?", "who_imposed"),
#                 # ("what are the victims?", "what_victims"),
#                 # ("what is the victim?", "what_victim"),
#             ]
#         )
#     if "judgment" in key:  # judgment
#         qs.extend(
#             [
#                 ("Who is the judge?", "who_judgment"),
#                 ("Who has emited the judgment?", "who_judgment"),
#                 ("Who has decided the judgment?", "who_judgment"),
#                 ("Who has settled the judgment?", "who_judgment"),
#                 ("Who entered in the judgment?", "who_judgment"),
#                 # ("what are the victims?", "what_victims"),
#                 # ("what is the victim?", "what_victim"),
#             ]
#         )
#     if "order" in key:  # order
#         qs.extend(
#             [
#                 ("Who has ordered something?", "who_judgment"),
#                 ("Who has decided the order?", "who_judgment"),
#                 ("Who is the orderer?", "who_order"),
#                 # ("what are the victims?", "what_victims"),
#                 # ("what is the victim?", "what_victim"),
#             ]
#         )
#     if "settl" in key:  # settl
#         qs.extend(
#             [
#                 ("Who has decided the settlement", "who_settled"),
#                 ("Who is the settler", "who_settled"),
#                 # ("Who are settled?", "who_settled"),
#                 # ("Who recieve an order?", "who_order"),
#                 # ("what are the victims?", "what_victims"),
#                 # ("what is the victim?", "what_victim"),
#             ]
#         )
#     if "charge" in key:  # charge
#         qs.extend(
#             [
#                 ("Who has charged?", "who_charged"),
#                 ("Who decide to charge?", "who_charged"),
#                 ("Who decide to inculpate?", "who_charged"),
#                 ("Who is the accusator?", "who_charged"),
#                 # ("what are the victims?", "what_victims"),
#                 # ("what is the victim?", "what_victim"),
#             ]
#         )
#     if "against" in key:  # against
#         qs.extend(
#             [
#                 ("Who is the prosecutor?", "who_victim"),
#                 ("Who are the prosecutors?", "who_victims"),
#                 # ("what are the victims?", "what_victims"),
#                 # ("what is the victim?", "what_victim"),
#             ]
#         )
#     if "violat" in key:  # viola
#         qs.extend(
#             [
#                 ("Who is the plaintiff?", "who_victim"),
#                 ("Who are the plaintiff?", "who_victims"),
#                 # ("what are the victims?", "what_victims"),
#                 # ("what is the victim?", "what_victim"),
#             ]
#         )

#     qs.extend(
#         [
#             ("What is the juriction?", "who_victim"),
#         ]
#     )

#     return qs


# def predict_juridiction(obj: dict, threshold: float = 0.4, n_sents: int = 4) -> list:
#     """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

#     # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
#     # win lots of time if the method is used in a loop with 100 predictions
#     nlpipe = obj["nlpipe"]

#     # pers_org_entities_list
#     # we will use this one later to make a filter at the end
#     pers_org_all = obj["pers_org_all"] + _u(_sub_you_shall_not_pass(obj["pers_org_all"]))
#     pers_org_all = _u(pers_org_all)

#     # items
#     # we will work on h1 and / or article but just 2 or 3 1st paragraphs
#     h1, abstract = obj["h1"], obj["abstract"]
#     abstract_sents = obj["abstract_sents"][:n_sents]
#     ans = []

#     # ask medhod
#     # here are the question answering and the true prediction built
#     for key_h1 in _question_helper(h1):
#         quest_pairs = _u(_question_selector(key_h1))
#         ans.extend(ask_all(h1, quest_pairs, nlpipe=nlpipe))

#     for sent in abstract_sents:
#         key_list = _question_helper(sent)
#         for key in key_list:
#             quest_pairs = _u(_question_selector(key))
#             ans.extend(ask_all(sent, quest_pairs, nlpipe=nlpipe))

#     # clean ans
#     # ans is a list of dict, each dict has keys such as answer, score etc
#     # for each answer we will clean this answer and create a new_answer more accurate
#     cleaned_ans = ans
#     answer_label = "answer"
#     if not len(cleaned_ans):
#         cleaned_ans = [{answer_label: "--None--", "score": -1}]

#     # merge ans
#     # based on new_answer we will make a groupby adding the scores for each new ans in a cumulative score
#     # example [{new_ans : hello, score:0.3},{new_ans : hello, score:0.3}, ]
#     # will become  [{new_ans : hello, score:0.6},]
#     merged_ans = merge_ans(cleaned_ans, label=answer_label)

#     # filert by spacy entities
#     # we are sure that a personn or an org is NOT a violation so
#     # if a prediction is in pers_org_entities_list, plz drop it
#     consitant_ans = [i for i in merged_ans if i[answer_label] in pers_org_all]

#     # filter by threshold
#     # we need to filter the score above which we consider that no a signe score but a
#     # cumulative score (much more strong, accurante and solid) will be droped
#     flatten_ans = [(i[answer_label], i["cum_score"]) for i in consitant_ans]
#     last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

#     return last_ans


# if __name__ == "__main__":

#     # import
#     import time
#     from legal_doc_processing.utils import get_pipeline, get_spacy
#     from legal_doc_processing.press_release.loader import press_release_X_y
#     from legal_doc_processing.press_release.press_release import PressRelease

#     # laod
#     nlpipe = get_pipeline()
#     nlspa = get_spacy()
#     nlspa.add_pipe("sentencizer")

#     # structured_press_release_r
#     df = press_release_X_y(features="defendant")
#     df = df.iloc[:7, :]
#     df["obj"] = [PressRelease(i, nlpipe=nlpipe, nlspa=nlspa) for i in df.txt.values]

#     # preds
#     t = time.time()
#     # 28 objects --> 181 secondes so --> +/-10 secondes per objects
#     df["pred_juridiction"] = df.obj.apply(lambda i: i.predict("juridiction"))
#     t = time.time() - t

#     # labels
#     preds_labels = list(df.preds.iloc[0].keys())
#     for k in preds_labels:
#         df["pred_" + k] = df.preds.apply(lambda i: i[k])

#     # 1st one
#     one = df.iloc[0, :]
#     one_txt = one.txt
#     one_ob = obj = self = one.obj