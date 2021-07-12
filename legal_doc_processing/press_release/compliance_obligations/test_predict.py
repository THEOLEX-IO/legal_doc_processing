from legal_doc_processing import logger
from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import merge_ans, ask_all

from legal_doc_processing.utils import get_pipeline, get_spacy
from legal_doc_processing.press_release.utils import press_release_X_y
from legal_doc_processing.press_release.press_release import (
    PressRelease,
    press_release_df,
)


if __name__ == "__main__":

    from legal_doc_processing import logger
    from legal_doc_processing.utils import uniquize as _u
    from legal_doc_processing.utils import merge_ans, ask_all

    from legal_doc_processing.utils import get_pipeline, get_spacy
    from legal_doc_processing.press_release.utils import press_release_X_y
    from legal_doc_processing.press_release.press_release import (
        PressRelease,
        press_release_df,
    )

    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    df = press_release_df(sample=1, nlspa=nlspa, nlpipe=nlpipe)
    is_coop = lambda i: "complian".lower() in str(i).lower()
    df_coop = df.loc[df.press_release_text.apply(is_coop), :]
    self = df_coop.pr.iloc[4]
    data = self.data

    sent_list = data.content_sents
    compliant_ok = lambda j: ("complian" in j.lower()) and ("obligat" in j.lower())
    compl_sent_list = [(i, j) for i, j in enumerate(sent_list) if compliant_ok(j)]
