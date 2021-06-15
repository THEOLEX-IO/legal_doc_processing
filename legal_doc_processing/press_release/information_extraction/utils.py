from itertools import product


def product_juridiction_pairs():

    cftc_cands = ["cftc", "Commodity Futures Trading Commission", "c.f.t.c"]
    doj_cands = ["doj", "department of justice", "d.o.j."]
    sec_cands = ["sec", "Securities and Exchange Commission", "s.e.c."]

    cands = dict()
    for k, _list in [("cftc", cftc_cands), ("doj", doj_cands), ("sec", sec_cands)]:
        dd = {i.lower().strip(): k.lower().strip() for i in _list}
        cands.update(dd)

    return cands


def product_juridic_form():
    """ make a list of llc, LLC, LLC. etc etc """

    # cands
    cands = ["inc", "llc", "ltd", "corp"]

    # conatiner
    llc_list = list()

    # for each
    for i in cands:
        # various case
        sample = [str(i), str(i).lower(), str(i).capitalize(), str(i).upper()]
        # case * -- point ou pas -- * --  espace, ou pas --
        sample = product(sample, [", ", " ", ""], [".", ""])
        sample = [str(j + i + k) for i, j, k in sample]
        # extend
        llc_list.extend(sample)

    # sorted reverse lengt
    llc_list = [(len(i), i) for i in llc_list]
    llc_list = sorted(llc_list, reverse=True, key=lambda i: i[0])
    llc_list = [i[1] for i in llc_list]

    return llc_list