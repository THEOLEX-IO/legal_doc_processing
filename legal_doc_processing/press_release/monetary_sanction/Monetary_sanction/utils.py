import pandas as pd
from transformers import pipeline
import numpy as np

nlp2 = pipeline("question-answering")
import os 


def _get_weight(question: str) -> float:
  a=0.0
  if (question=="How much is ordered to pay as monetary sanction?"):
    a= 7.744
  elif (question== "How much is restituate?"):
    a= 6.888999999999999
  elif (question== "How much is the monetary sanction?"):
    a= 6.241000000000001
  elif (question == "What is ordered?"):
    a= 1.444
  elif (question== "What is restituate?"):
    a= 1.444
  return a


import logging
logger = logging.getLogger()


def _cast_as_int(cleaned_ans):
    """transform a list of numbers in ints """

    MULTI = [("nmillion", 1_000_000), ("thousand", 1000), ("million", 1_000_000), ("billion", 1_000_000_000)]

    cleaned_ans = [i.lower().strip() for i in cleaned_ans]

    # delette € or $
    cleaned_ans = [
        i.replace("$", "").replace("€", "").replace("£", "").replace("\\", "") for i in cleaned_ans
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
        .replace("nmillions", "nmillion")
        .replace("millions", "million")
        .replace("billions", "billion")
        .replace("hundreds", "hundred")
        for i in cleaned_ans
    ]
    # logger.info(f"cleaned_ans: {cleaned_ans} ")

    cleaned_ans_multi = []
    for ans in cleaned_ans:
        multi = ""
        for k, _ in MULTI:
            if k in ans:
                multi = k
                break

        cleaned_ans_multi.append((ans, multi))

    # logger.info(f"cleaned_ans_multi: {cleaned_ans_multi} ")

    cleaned_ans_multi_2 = []
    for numb, multi in cleaned_ans_multi:
        if not multi:
            # dump centimies
            numb = numb.split(".")[0]
            # easy, jsute keep the numbers
            numb = "".join([c for c in list(numb) if c.isnumeric()])
            if (numb==""):
              numb = 0
            else:
              numb = int(numb)
        else:
            # clean the numb: 1, 12 -> 1.22
            numb = numb.split(multi)[0].replace(",", ".").strip()

            # find last numberic and clean : a total of 3.12 -> 3.12
            try:
                cands_list = [i for i in numb.split(" ") if i[0].isnumeric()]
                cand = cands_list[-1].strip()
            except:
                continue#raise AttributeError(f"{cands_list} ")

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
