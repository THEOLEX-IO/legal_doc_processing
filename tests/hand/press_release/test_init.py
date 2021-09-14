from time import time
from legal_doc_processing import logger
from legal_doc_processing.utils import get_pipeline, get_spacy
from legal_doc_processing.press_release.utils import press_release_X_y
from legal_doc_processing.press_release.press_release import (
    PressRelease,
    press_release_df,
)


if __name__ == "__main__":

    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # auth_list = ["cftc", "cfbp", "doj", "sec"]
    # _ = [test_preds(i, sample=0.1, nlspa=nlspa, nlpipe=nlpipe) for i in auth_list]

    df = press_release_df(sample=1, nlspa=nlspa, nlpipe=nlpipe)

    sent_funct = lambda pr: [
        i.text for i in nlspa(pr.struct_text["article"]).sents if i.text.strip()
    ]

    # df["sents"] = df.pr.apply(sent_funct)

    # coop_fuct = lambda sent_list: any(
    #     [("coopera" in i) and ("credit" in i) for i in sent_list]
    # )
    # idxs = df.sents.apply(coop_fuct)

    # coop_df = df.loc[idxs, :]

    # txt = """The criminal monetary penalty for Novartis Greece reflects a 25 percent reduction off a point near the midpoint of the U.S. Sentencing
    # Guidelines range because, although Novartis Greece fully cooperated and remediated, its parent company Novartis AG was involved in similar
    # conduct for which it previously reached a resolution with the SEC in March 2016."""

    # from legal_doc_processing.utils import ask_all

    # quest_pairs = [("what is the reduction due to cooperation?", "coop")]

    # ans = ask_all(txt, quest_pairs, nlpipe)
