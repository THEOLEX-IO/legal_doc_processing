import pandas as pd
from transformers import pipeline
import numpy as np

nlp2 = pipeline("question-answering")
import os 


def _get_dict_weighted() -> dict:
    """based on a key from _question helper find the list of good question to ask """


    Liste_ordered = [
                     #high
                     "How much is ordered to pay as monetary sanction?",
                     "How much is restituate?",
                     

                     #middle

                     "How much is the monetary sanction?",


                     

                     #low
                     "What is ordered?",
                     "What is restituate?"

    ]

    # make sure there is no repetition
    Liste_ordered = Liste_ordered

    nb_items = len(Liste_ordered) #nb of questions
    t=[0.88, 0.83, 0.79, 0.38, 0.38]
    liste_weights = list(10*(np.power(t,2))) #get weights from 1 to 20


    #add weight to questions and put them into a dictionnary
    Dict_weighted = {Liste_ordered[i]:liste_weights[i] for i in range(nb_items)}

    return Dict_weighted


def _get_weight(question: str) -> float:
    """
    input: question 
    output: score associated 
    usage: _get_weight("who is ordered?")
    """
    Dict_weighted = _get_dict_weighted()
    try:
      return Dict_weighted[question] #return weight
    except:
      get_list_key = lambda x: [elt for elt in x.replace("?","").lower().split(" ") if elt]
      for quest in Dict_weighted:
        if set(get_list_key(question))==set(get_list_key(quest)):
          return Dict_weighted[quest]
      return 0




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
