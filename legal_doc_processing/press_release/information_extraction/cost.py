import pandas as pd

from legal_doc_processing.utils import (
    _if_not_pipe,
    _ask,
)


def _ask_all(txt, nlpipe) -> list:
    """asl all questions and return a list of dict """

    # pipe
    nlpipe = _if_not_pipe(nlpipe)

    # ans
    ans = []

    # question, funct
    quest_pairs = [
        ("How much it will cost", "ask_how_cost"),
        ("Who many dollars", "ask_how_dollars"),
        ("What is the cost?", "ask_what_cost"),
    ]

    # loop
    for quest, label in quest_pairs:
        ds = _ask(txt=txt, quest=quest, nlpipe=nlpipe)
        _ = [d.update({"question": label}) for d in ds]
        ans.extend(ds)

    # sort
    ans = sorted(ans, key=lambda i: i["score"], reverse=True)

    # clean
    ans = [i for i in ans if (i["answer"].lower() != "defendants")]

    return ans


def _clean_ans(ans, threshold=0.5):
    """ """

    # build dataframe
    df = pd.DataFrame(ans)
    df = df.loc[:, ["score", "answer"]]

    # group by ans and make cumutavie score of accuracy
    ll = [
        {"answer": k, "cum_score": v.score.sum()}
        for k, v in df.groupby("answer")
        if v.score.sum() > threshold
    ]
    ll = sorted(ll, key=lambda i: i["cum_score"], reverse=True)

    return ll


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


def predict_cost(structured_press_release: list, nlpipe=None):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe
    nlpipe = _if_not_pipe(nlpipe)

    # section cands
    cands = [
        structured_press_release["h1"].lower(),
        structured_press_release["h2"].lower(),
        # article = structured_press_release["article"].lower()
    ]

    # section ok if "pay" or amend or $ or € or euro in the text
    money = ["$", "€", "£", "euros", "dollar", "livre"]
    is_good = (
        lambda sec: ("amend" in sec)
        or ("penalty" in sec)
        or ("pay" in sec)
        or sum([i for i in money if i.replace("s", "") in sec])
    )

    # parse sections to know if ok
    txt = ""
    for section in cands:
        txt = section if is_good(section) else ""
        if txt:
            break

    # if  nothing ok
    if not txt:
        return "--None--"

    # ask all and get all possible response
    ans = _ask_all(txt, nlpipe)

    # group by ans, make cumulative sum of accuracy for eash ans and filter best ones
    ll = _clean_ans(ans)

    # keep ans
    cleaned_ans = [i["answer"] for i in ll]

    # cast as int
    cleaned_ans = _cast_as_int(cleaned_ans)

    # reponse
    resp = ", ".join(cleaned_ans)

    return resp


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import *
    from legal_doc_processing.press_release.utils import load_press_release_text_list
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # pipe
    nlpipe = get_pipeline()

    # structured_press_release_list
    press_txt_list = load_press_release_text_list()
    structured_press_release_list = [structure_press_release(i) for i in press_txt_list]

    # test one
    structured_press_release = structured_press_release_list[0]

    all_ans_h1 = _ask_all(structured_press_release["h1"], nlpipe)
    all_ans_h2 = _ask_all(structured_press_release["h2"], nlpipe)
    all_ans_article = _ask_all(structured_press_release["article"], nlpipe)

    ans = predict_cost(structured_press_release, nlpipe)

    # test others
    ans_list = [predict_cost(p, nlpipe) for p in structured_press_release_list]

    clean_ans_list = [[d["answer"] for d in ll] for ll in ans_list]
    clean_ans_list = [", ".join(ll) for ll in clean_ans_list]
