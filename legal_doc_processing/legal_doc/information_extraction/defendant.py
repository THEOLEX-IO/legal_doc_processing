from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all

from legal_doc_processing.legal_doc.clean.defendant import (
    clean_ans,
    _sub_you_shall_not_pass,
)


def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = list()

    if "accused" in _txt:
        res.append("accused")
    if "defendant" in _txt:
        res.append("defendant")
    if "violate" in _txt:
        res.append("violate")
    if "against" in _txt:
        res.append("against")
    if "filed" in _txt:
        res.append("filed")
    if "judgement" in _txt:
        res.append("judgement")
    if "complaint" in _txt:
        res.append("complaint")

    return res


def _question_selector(key: str) -> list:
    """based on a key from _question helper find the list of good question to ask """

    qs = list()

    if "defendant" in key:
        qs.extend(
            [
                ("Who is the defendant?", "who_defendant"),
                ("Who are the defendants?", "who_defendants"),
                # ("what are the defendants?", "what_defendant"),
                # ("what is the defendant?", "what_defendant"),
            ]
        )
    if "violat" in key:
        qs.extend(
            [
                ("Who is the violator?", "what_violator"),
                ("Who have made the violation?", "what_violator"),
                ("Who has made the violation?", "what_violator"),
                ("Who are the violators?", "what_violators"),
                # ("What is the violator?", "what_violator"),
                # ("What are the violators?", "what_violators"),
            ]
        )
    if "against" in key:
        qs.extend(
            [
                ("Who is the victim", "what_against"),
                ("Against who is the action?", "what_against"),
                ("Who is the action against to?", "what_against"),
                ("Against who?", "what_againsts"),
                # ("What is the violator?", "what_violator"),
                # ("What are the violators?", "what_violators"),
            ]
        )
    if "filed" in key:
        qs.extend(
            [
                ("Who recieve a complaint?", "what_violator"),
                ("Who is accused?", "what_violator"),
                ("Against who is the complaint?", "what_violator"),
                # ("Who are the violators?", "what_violators"),
                # ("What is the violator?", "what_violator"),
                # ("What are the violators?", "what_violators"),
            ]
        )
    if "judgement" in key:
        qs.extend(
            [
                ("Who is pursued?", "what_judgement"),
                ("Who is inculpated?", "what_judgement"),
                ("Who is under judgement?", "what_judgement"),
                ("Who is accused?", "what_judgement"),
                ("Against who is the judgement?", "what_judgement"),
                # ("What is the violator?", "what_violator"),
                # ("What are the violators?", "what_violators"),
            ]
        )
    if "complaint" in key:
        qs.extend(
            [
                ("Who is accused?", "what_judgement"),
                ("Who is inculpated?", "what_judgement"),
                ("Who is under judgement?", "what_judgement"),
                ("Who recieved a complaint ?", "what_judgement"),
                ("Against who is the complaint?", "what_judgement"),
            ]
        )
    return qs


def predict_defendant(obj: dict, threshold=0.2, n_sents: int = 5) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
    # win lots of time if the method is used in a loop with 100 predictions
    nlpipe, nlspa = obj["nlpipe"], obj["nlspa"]

    # pers_org_all
    # we will use this one later to make a filter at the end
    pers_org_all = obj["pers_org_all"] + [
        _sub_you_shall_not_pass(i) for i in obj["pers_org_all"]
    ]
    pers_org_all = _u(pers_org_all)

    # items
    # we will work on h1 and / or article but just 2 or 3 1st paragraphs
    h1, abstract = obj["h1"], obj["abstract"]
    # print(abstract)
    abstract_sents = obj["abstract_sents"][:n_sents]
    # print(abstract_sents)
    ans = []

    # ask method
    # for each sentence
    for sent in abstract_sents:
        input(f"sent : {sent}")
        key_list = _question_helper(sent)
        input(f"key_list:{key_list} ")
        for key in key_list:
            # from key to questions and from questions to answers
            quest_pairs = _u(_question_selector(key))
            input(f"quest_pairs:{quest_pairs} ")
            _ans = ask_all(sent, quest_pairs, nlpipe=nlpipe)
            input(f"_ans[:10] : {_ans[:10]} ")
            ans.extend(_ans)

    # clean ans
    # ans is a list of dict, each dict has keys such as answer, score etc
    # for each answer we will clean this answer and create a new_answer more accurate
    cleaned_ans = clean_ans(ans)
    answer_label = "new_answer"
    if not len(cleaned_ans):
        cleaned_ans = [{answer_label: "--None--", "score": -1}]

    # merge ans
    # based on new_answer we will make a groupby adding the scores for each new ans in a cumulative score
    # example [{new_ans : hello, score:0.3},{new_ans : hello, score:0.3}, ]
    # will become  [{new_ans : hello, score:0.6},]
    merged_ans = merge_ans(cleaned_ans, label=answer_label)

    # filert by spacy entities
    # we are sure that a personn or an org is NOT a violation so
    # if a prediction is in pers_org_entities_list, plz drop it
    consitant_ans = [i for i in merged_ans if i[answer_label] in pers_org_all]

    # filter by threshold
    # we need to filter the score above which we consider that no a signe score but a
    # cumulative score (much more strong, accurante and solid) will be droped
    flatten_ans = [(i[answer_label], i["cum_score"]) for i in consitant_ans]
    last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

    return last_ans


if __name__ == "__main__":

    # import
    import time
    from legal_doc_processing.utils import get_pipeline, get_spacy
    from legal_doc_processing.legal_doc.loader import legal_doc_X_y
    from legal_doc_processing.legal_doc.legal_doc import LegalDoc

    # laod
    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # data
    hreshold = 0.2
    n_sents = 7

    # structured_press_release_r
    df = legal_doc_X_y(features="defendant")
    df = df.iloc[:2, :]
    df["obj"] = [LegalDoc(i, nlpipe=nlpipe, nlspa=nlspa) for i in df.txt.values]

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["pred_defendant"] = df.obj.apply(lambda i: i.predict("defendant"))
    t = time.time() - t

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ob = self = one.obj
    obj = self.data_