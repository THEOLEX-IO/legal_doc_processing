from transformers import pipeline
nlp2 = pipeline("question-answering")

import pandas as pd
import numpy as np 
import os
import re
import requests

def _del_dummy_breaklines(txt: str):

  new_txt = (
      txt.replace("\n.", "$$$$")
      .replace("\n", " ")
      .replace("  ", " ")
      .replace("  ", " ")
      .replace("  ", " ")
      .replace("$$$$", "\n")
  )

  return new_txt


def _del_bouble_breaks_and_spaces(txt: str) -> str:

  new_txt = (
      txt.replace("\n\n", "\n")
      .replace("\n\n", "\n")
      .replace("\n\n", "\n")
      .replace("\n\n", "\n")
      .replace("\n\n", "\n")
      .replace("\n\n", "\n")
      .replace("\n\n", "\n")
      .replace("  ", " ")
      .replace("  ", " ")
      .replace("  ", " ")
      .replace("  ", " ")
      .replace("  ", " ")
      .replace("  ", " ")
      .replace("  ", " ")
      .replace("  ", " ")
      .replace("\n\n", "\n")
      .replace("\n\n", "\n")
      .replace("\n\n", "\n")
      .replace("\n\n", "\n")
      .replace("\n\n", "\n")
      .replace("\n\n", "\n")
  )

  return new_txt

def _u(liste):
  return list(set(liste))

def _question_helper(txt) -> list:

        _txt = txt.lower()
        res = []

        cands = [
            "impose",
            "judgment",
            "order",
            "settl",
            "defendant",
            "charge",
            "against",
            "violate",
        ]

        for cand in cands:
            if cand in _txt:
                res.append(cand)

        return res

def _question_selector(key: str) -> list:
        """based on a key from _question helper find the list of good question to ask """

        res = []

        if "impose" in key:  # impose
            res.extend(
                [
                    ("Who is imposed?", "who_imposed"),
                    ("Who are imposed?", "who_imposed"),
                    # ("what are the victims?", "what_victims"),
                    # ("what is the victim?", "what_victim"),
                ]
            )
        if "judgment" in key:  # judgment
            res.extend(
                [
                    ("Who is under judgment?", "who_judgment"),
                    ("Who are under judgment?", "who_judgment"),
                    ("Who is convicted", "who_convicted"),
                    ("Who are convicted?", "who_convicted"),
                    # ("what are the victims?", "what_victims"),
                    # ("what is the victim?", "what_victim"),
                ]
            )

        if "order" in key:  # order
            res.extend(
                [
                    ("Who is ordered", "who_judgment"),
                    ("Who are ordered?", "who_judgment"),
                    ("Who recieve an order?", "who_order"),
                    # ("what are the victims?", "what_victims"),
                    # ("what is the victim?", "what_victim"),
                ]
            )

        if "settl" in key:  # settl
            res.extend(
                [
                    ("Who recieve a settlement", "who_settled"),
                    # ("Who are settled?", "who_settled"),
                    # ("Who recieve an order?", "who_order"),
                    # ("what are the victims?", "what_victims"),
                    # ("what is the victim?", "what_victim"),
                ]
            )

        if "defendant" in key:  # defendant
            res.extend(
                [
                    ("Who is the defendant?", "who_defendant"),
                    ("Who are the defendants?", "who_defendants"),
                    ("What is the defendant?", "what_defendant"),
                    ("What are the defendants?", "what_defendants"),
                ]
            )

        if "charge" in key:  # charge
            res.extend(
                [
                    ("Who is charged", "who_charged"),
                    ("Who are charged?", "who_charged"),
                    # ("what are the victims?", "what_victims"),
                    # ("what is the victim?", "what_victim"),
                ]
            )

        if "against" in key:  # against
            res.extend(
                [
                    ("Who is the victim?", "who_victim"),
                    ("Who are the victims?", "who_victims"),
                    # ("what are the victims?", "what_victims"),
                    # ("what is the victim?", "what_victim"),
                ]
            )

        if "defendant" in key:  # defendant
            res.extend(
                [
                    ("Who is the defendant?", "who_defendant"),
                    ("Who are the defendants?", "who_defendants"),
                    # ("what are the defendants?", "what_defendant"),
                    # ("what is the defendant?", "what_defendant"),
                ]
            )

        if "violate" in key:  # violated
            res.extend(
                [
                    #
                    ("Who is the violator?", "who_violator"),
                    ("Who are the violators?", "who_violators"),
                    ("What is the violator?", "what_violator"),
                    ("What are the violators?", "what_violators"),
                    ("Who has violated?", "who_violated"),
                    ("Who made the violations?", "who_violation"),
                ]
            )

        return res


def _question_lister(key_list: list) -> list:
        """from key_list return question list """

        question_list = []
        for key in key_list:
            question_list.extend(_question_selector(key))

        return _u(question_list)

def get_questions(texte:str):
        """ """
        l_questions = []
        cands_seleted = _question_helper(texte)
        return _question_lister(cands_seleted)


def _get_dict_weighted() -> dict:
    """based on a key from _question helper find the list of good question to ask """

    Liste_ordered = [
                     #high
                     "Who is the defendant?",
                     "Who are the defendants?",
                     

                     #middle
                     
                     "Who are ordered?",
                     "What are the defendants?",
                     "Who is imposed?",

                     #unexplainable good result
                     "Who are charged?",
                     "Who recieve a settlement",
                     "Who is the victim?",
                     "Who is charged",
                     "Who are the victims?",

                     #others
                     "Who are under judgment?",
                     "Who is under judgment?",
                     "Who is convicted",
                     "Who are convicted?",
                     "Who is the violator?",
                     "Who are the violators?",
                     "What is the violator?",
                     "What are the violators?",
                     "Who has violated?",
                     "Who made the violations?",
                     "Who recieve an order?", #confusing
                     

                     #low
                     "Who is ordered?",
                     "Who are imposed?",
                     "What is the defendant?"

    ]

    # make sure there is no repetition
    Liste_ordered = Liste_ordered

    nb_items = len(Liste_ordered) #nb of questions
    liste_weights = list(10*(np.power(np.linspace(0,1,nb_items),2)))[::-1] #get weights from 1 to 20


    #add weight to questions and put them into a dictionnary
    Dict_weighted = {Liste_ordered[i]:liste_weights[i] for i in range(nb_items)}

    return Dict_weighted


def _get_weight(question: str,Dict_weighted=None) -> float:
    """
    input: question 
    output: score associated 
    usage: _get_weight("who is ordered?")
    """
    if not Dict_weighted: Dict_weighted = _get_dict_weighted()
    try:
      return Dict_weighted[question] #return weight
    except:
      get_list_key = lambda x: [elt for elt in x.replace("?","").lower().split(" ") if elt]
      for quest in Dict_weighted:
        if set(get_list_key(question))==set(get_list_key(quest)):
          return Dict_weighted[quest]
      return 0
