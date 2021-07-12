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

    txt = "it took place in France"

    label = "GPE"

    ans = [i for i in nlspa(txt).ents if i.label_ == label]
    ans = [str(p) for p in ans]