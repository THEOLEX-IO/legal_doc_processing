from itertools import product


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