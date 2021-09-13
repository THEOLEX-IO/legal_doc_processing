from time import time
from legal_doc_processing import logger

from legal_doc_processing.utils import get_spacy

from legal_doc_processing.press_release.structure.cftc import (
    structure_press_release as structure_cftc,
)
from legal_doc_processing.press_release.structure.doj import (
    structure_press_release as structure_doj,
)

from legal_doc_processing.press_release.structure.cfbp import (
    structure_press_release as structure_cfbp,
)

from legal_doc_processing.press_release.structure.sec import (
    structure_press_release as structure_sec,
)
# import pdb;pdb.set_trace()

from time import time
from legal_doc_processing import logger
from legal_doc_processing.utils import get_spacy
nlspa = get_spacy()
# nlspa.add_pipe("sentencizer")
auth_list = ["cftc", "cfbp", "doj", "sec"]
juridictions = ["cftc", "cfbp", "doj", "sec"]

def test_structure(sample=0.99, nlspa=""):
    """ """

    for juridiction in juridictions:
        assert juridiction in ["cftc", "cfbp", "doj", "sec"]

        from time import time
        from legal_doc_processing import logger

        logger.info("called")

        # load
        logger.info("load")
        from legal_doc_processing.utils import get_spacy

        if not nlspa:
            nlspa = get_spacy()
        try:
            nlspa.add_pipe("sentencizer")
        except Exception as e:
            pass

        # dataframe
        logger.info("dataframe")
        from legal_doc_processing.press_release.utils import press_release_X_y

        df = press_release_X_y(juridiction=juridiction, sample=sample)
        cols = ["folder", "press_release_text"]
        df = df.loc[:, cols]

        # choose funct
        logger.info("choose funct")
        if juridiction == "cftc":
            struct_funct = structure_cftc
        if juridiction == "doj":
            struct_funct = structure_doj
        if juridiction == "sec":
            struct_funct = structure_sec
        if juridiction == "cfbp":
            struct_funct = structure_cfbp

        # structure
        logger.info("structure")
        struct_ = lambda i: struct_funct(i, nlspa=nlspa)
        df["dd"] = df.press_release_text.apply(struct_)

        # extrcat cols
        logger.info("extrcat cols")
        col_list = list(df.dd.iloc[0].keys())
        for col in col_list:
            df["dd_" + col] = df.dd.apply(lambda i: i.get(col, -42))
        df.drop("dd", inplace=True, axis=1)
        # import pdb;pdb.set_trace()
        # save
        logger.info("save")
        fn = f"./tmp/structure_press_release_{juridiction}_{len(df)}_lines.csv"
        df.to_csv(fn, index=False)


# if __name__ == "__main__":
#     import pdb;pdb.set_trace()
#     from time import time
#     from legal_doc_processing import logger
#     from legal_doc_processing.utils import get_spacy

#     nlspa = get_spacy()
#     nlspa.add_pipe("sentencizer")

#     auth_list = ["cftc", "cfbp", "doj", "sec"]
#     import pdb;pdb.set_trace()
    # _ = [test_structure(i, sample=0.99, nlspa=nlspa) for i in auth_list]
