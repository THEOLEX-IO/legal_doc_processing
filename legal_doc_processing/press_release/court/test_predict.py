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

    df = press_release_df("cftc", sample=1, nlspa=nlspa, nlpipe=nlpipe)
    is_court = lambda i: "court".lower() in str(i).lower()
    df_court = df.loc[df.press_release_text.apply(is_court), :]
    self = df_court.pr.iloc[0]
    data = self.data

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents
    coop_sent_list = [(i, j) for i, j in enumerate(sent_list) if "cooperat" in j.lower()]
