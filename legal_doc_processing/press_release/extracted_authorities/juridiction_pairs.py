juridiction_dict = {
    "cftc": "cftc",
    "commodity futures trading commission": "cftc",
    "c.f.t.c": "cftc",
    "the commodity futures trading commission": "cftc",
    "the cftc": "cftc",
    "doj": "doj",
    "department of justice": "doj",
    "d.o.j.": "doj",
    "the department of justice": "doj",
    "the doj": "doj",
    "sec": "sec",
    "securities and exchange commission": "sec",
    "s.e.c.": "sec",
    "the securities and exchange commission": "sec",
    "the sec": "sec",
    "the consumer financial protection bureau": "cfpb",
    "cfpb": "cfpb",
    "consumer financial protection bureau": "cfpb",
    "the cfpb": "cfpb",
    "c.f.p.b": "cfpb",
}


def product_juridiction_pairs():

    cftc_cands = [
        "cftc",
        "Commodity Futures Trading Commission",
        "c.f.t.c",
        "the Commodity Futures Trading Commission",
        "the cftc",
    ]
    doj_cands = [
        "doj",
        "department of justice",
        "d.o.j.",
        "the department of justice",
        "the doj",
    ]
    sec_cands = [
        "sec",
        "Securities and Exchange Commission",
        "s.e.c.",
        "the Securities and Exchange Commission",
        "the sec",
    ]

    cfpb_cands = [
        "The Consumer Financial Protection Bureau",
        "cfpb",
        "Consumer Financial Protection Bureau",
        "the cfpb",
        "c.f.p.b",
    ]

    cands = dict()
    for k, _list in [
        ("cftc", cftc_cands),
        ("doj", doj_cands),
        ("sec", sec_cands),
        ("cfpb", cfpb_cands),
    ]:
        dd = {i.lower().strip(): k.lower().strip() for i in _list}
        cands.update(dd)

    return cands