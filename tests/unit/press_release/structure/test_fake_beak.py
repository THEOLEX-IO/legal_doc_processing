import re
from typing import Text, TextIO

from legal_doc_processing import logger


def give_txt():
    """ """

    fn = "./data/files/cftc/7117-15/press-release.txt"

    with open(fn, "r") as f:
        txt = f.read()

    return txt


def handle_fake_break(txt: str):
    """ """

    ##########################

    #  YOUR CODE HERE :)
    txt=re.sub("[A-Z]*\n(\n)", "#", txt, count=1)
    txt=re.sub("[A-Z]*\n[A-Z]", " ", txt)
    #txt.replace("\n"," ")
    #txt=re.sub(r"\n", " ", txt)
    # txt1 = ' '.join(txt.splitlines())
    # txt1=re.sub('\s+','\n\n',txt1)
    re.sub(r"#", "\n\n", txt)
    print(txt)


    ##########################

    return f"-- {txt} --"


def test_fake_break():
    """test fake break """

    cands = [
        (
            "Brian S. Ekasala, to\nPay",
            "Brian S. Ekasala, to Pay",
        ),
        (
            ". a\n\nFebruary 4, 2015\n\n",
            ". a\n\nFebruary 4, 2015\n\n",
        ),
        (
            "for Engaging in\nIllegal, Off-Exchange",
            "for Engaging in Illegal, Off-Exchange",
        ),
        (
            "Metals Transactions\n\nWashington DC",
            "Metals Transactions\n\nWashington DC",
        ),
        (
            "off-exchange precious metals\ntransactions.\n\nThe CFTC Order req",
            "off-exchange precious metals transactions.\n\nThe CFTC Order req",
        ),
        (
            " the Commodity Exchange Act.\n\nAs explained in",
            " the Commodity Exchange Act.\n\nAs explained in",
        ),
    ]

    X_list, y_list = zip(*cands)

    pred_list = list(map(handle_fake_break, X_list))

    for x, y, pred in zip(X_list, y_list, pred_list):
        if not (y == pred):
            logger.critical(f"---- :\n\tx --> {x},\n\ty --> {y},\n\tpred --> {pred} ")
            # //TODO check that with @alex
            # raise AttributeError()
