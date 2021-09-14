juridiction_dict = {
    # cftc
    "the cftc": "cftc",
    "cftc": "cftc",
    "c.f.t.c": "cftc",
    "the commodity futures trading commission": "cftc",
    "commodity futures trading commission": "cftc",
    # doj
    "the doj": "doj",
    "doj": "doj",
    "d.o.j.": "doj",
    "the department of justice": "doj",
    "department of justice": "doj",
    # sec
    "the sec": "sec",
    "sec": "sec",
    "s.e.c.": "sec",
    "the securities and exchange commission": "sec",
    "securities and exchange commission": "sec",
    # cfpb
    "the cfbp": "cfbp",
    "the cfpb": "cfbp",
    "cfbp": "cfbp",
    "cfpb": "cfbp",
    "c.f.p.b": "cfbp",
    "the consumer financial protection bureau": "cfbp",
    "consumer financial protection bureau": "cfbp",
}


def product_juridiction_pairs():

    cftc_cands = [
        "the cftc",
        "cftc",
        "c.f.t.c",
        "the Commodity Futures Trading Commission",
        "Commodity Futures Trading Commission",
    ]
    doj_cands = [
        "the doj",
        "doj",
        "d.o.j.",
        "the department of justice",
        "department of justice",
    ]
    sec_cands = [
        "the sec",
        "sec",
        "s.e.c.",
        "the Securities and Exchange Commission",
        "Securities and Exchange Commission",
    ]

    cfbp_cands = [
        "the cfbp",
        "the cfpb",
        "cfbp",
        "cfpb",
        "c.f.p.b",
        "Consumer Financial Protection Bureau",
        "the Consumer Financial Protection Bureau",
    ]

    cands = {}
    for k, _list in [
        ("cftc", cftc_cands),
        ("doj", doj_cands),
        ("sec", sec_cands),
        ("cfbp", cfbp_cands),
    ]:
        dd = {i.lower().strip(): k.lower().strip() for i in _list}
        cands.update(dd)

    return cands