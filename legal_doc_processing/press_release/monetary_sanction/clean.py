from legal_doc_processing import logger

# def _get_entities_money(obj: dict) -> list:
#     """get entities MONEY from h1 and sub_article """

#     nlspa = obj["nlspa"]

#     # sub article

#     # all pers all orgs from spacy entities
#     all_money = _u(obj["cost_all"])

#     # clean
#     all_init_money = _cast_as_int(all_money)
#     all_init_money = _u(all_init_money)

#     return all_init_money


def _cast_as_int(cleaned_ans):
    """transform a list of numbers in ints """

    MULTI = [("thousand", 1000), ("million", 1_000_000), ("billion", 1_000_000_000)]

    cleaned_ans = [i.lower().strip() for i in cleaned_ans]

    # delette € or $
    cleaned_ans = [
        i.replace("$", "").replace("€", "").replace("£", "") for i in cleaned_ans
    ]
    # logger.info(f"cleaned_ans: {cleaned_ans} ")

    # SPECIAL CASE :hundred of million
    spec_case = (
        lambda i: i.replace("hundred of", "100").strip()
        if "hundred of million" in i
        else i
    )
    cleaned_ans = [spec_case(i) for i in cleaned_ans]

    # SPECIAL CASE 100.000.000 usd
    spec_case = lambda i: i.replace(".", ",").strip() if (i.count(".") > 1) else i
    cleaned_ans = [spec_case(i) for i in cleaned_ans]

    # thousands as thousand
    cleaned_ans = [
        i.replace("thousands", "thousand")
        .replace("millions", "million")
        .replace("billions", "billion")
        .replace("hundreds", "hundred")
        for i in cleaned_ans
    ]
    # logger.info(f"cleaned_ans: {cleaned_ans} ")

    cleaned_ans_multi = list()
    for ans in cleaned_ans:
        multi = ""
        for k, _ in MULTI:
            if k in ans:
                multi = k
                break

        cleaned_ans_multi.append((ans, multi))

    # logger.info(f"cleaned_ans_multi: {cleaned_ans_multi} ")

    cleaned_ans_multi_2 = list()
    for numb, multi in cleaned_ans_multi:
        if not multi:
            # dump centimies
            numb = numb.split(".")[0]
            # easy, jsute keep the numbers
            numb = "".join([c for c in list(numb) if c.isnumeric()])
            numb = int(numb)
        else:
            # clean the numb: 1, 12 -> 1.22
            numb = numb.split(multi)[0].replace(",", ".").strip()

            # find last numberic and clean : a total of 3.12 -> 3.12
            try:
                cands_list = [i for i in numb.split(" ") if i[0].isnumeric()]
                cand = cands_list[-1].strip()
            except:
                raise AttributeError(f"{cands_list} ")

            # specific a 'total of for 3 000' ->  '3000'
            try:
                if cands_list[-2].strip()[0].isnumeric():
                    cand = str(cands_list[-2].strip()) + str(cand)
            except Exception as e:
                pass

            numb = float(cand.strip())

            # make 1.3 million -> 1.3 * 1 000 000 = 1 300 000
            for mm, k in MULTI:
                if mm == multi:
                    numb *= k

        cleaned_ans_multi_2.append(int(numb))

    logger.info(f"cleaned_ans_multi_2: {cleaned_ans_multi_2} ")

    return cleaned_ans_multi_2
