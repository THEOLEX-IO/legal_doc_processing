from transformers import pipeline
nlp2 = pipeline("question-answering")

import pandas as pd
import numpy as np 
import os
import re
import requests
def _del_bouble_breaks_and_spaces(txt: str) -> str:

  x = re.sub("[\n]*", "", txt)
  x1= re.sub("  ", " ",x)
  return x1

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
      return Dict_weighted[question]
    except:
      get_list_key = lambda x: [elt for elt in x.replace("?","").lower().split(" ") if elt]
      for quest in Dict_weighted:
        if set(get_list_key(question))==set(get_list_key(quest)):
          return Dict_weighted[quest]
      return 0

def convert(lst, i):
    return lst[i].split()

def delete_uni(liste):
  i=0
  while (i < len(liste)):
    j=0
    while (j < len(liste)):
      if (i==j):
        j += 1
        continue
      l1= convert(liste, i)
      l2=convert(liste, j)
      t=0
      for k in l1:
        if (k in l2):
          t+=1
      if (t==len(l1)):
        del liste[i]
        i=0
        j=0
      else:
        j+=1
    i+=1
  return liste

def give_answer(df_of_top):
  liste=[]
  l=[]
  df_of_topp = df_of_top.groupby(["folder"])
  for key,item in df_of_topp:
    fichiers = df_of_topp.get_group(key)
    fichiers = fichiers.reset_index(drop=True)
    longueur=len(fichiers)
    i=0
    while (i < longueur):
      line=fichiers.loc[i, ["folder", "answer", "context", "score"]]
      t=fichiers.at[i, 'answer']
      s=str(t)
      u= _del_bouble_breaks_and_spaces (s)
      liste.append(u)
      i+=1
  liste = _u(liste)
  liste=delate_uni(liste)
  liste = [elt for elt in liste if type(elt)!=type(3.5)]
  answer= ';'.join(liste)
  l.append(answer)
  return l

def best_predict(df_res):
   #transform df in df_grouped in order to display together result for different N
  df_res_grouped = df_res.groupby(["folder","tag","question"]) #grouper les lignes par fichier et question
  df_res_copy = pd.DataFrame(columns=df_res.columns) #créer un nouveau dataframe
  for key,item in df_res_grouped: #parcourir les groupes
    a_group = df_res_grouped.get_group(key) #trouver les lignes du groupe
    df_res_copy = df_res_copy.append(a_group) #ajouter les lignes au nouveau dataframe
  #ajout de la colonne norme_score
  df_res_copy['norm_score'] = np.nan
  for i in range(len(df_res_copy)):
    question = df_res_copy.loc[i,"question"]
    weight = _get_weight(question)
    answer = df_res_copy.loc[i,"answer"]
    folder = df_res_copy.loc[i,"folder"]
    if 'defendant' in answer.lower():
      weight=0
    if 'judge' in answer.lower(): 
      weight=0
    if 'order' in answer.lower():
      weight=0
    #compute score
    score = df_res_copy.loc[i,'score']
    df_res_copy.loc[i,'norm_score'] = weight*np.sqrt(score)
  
    #recherche du  top et création du dataframe contenant le top3+ best normal
  log=False
  #transform df in df_grouped in order to
  df_res_copy_grouped = df_res_copy.groupby(["folder"]) #grouper les lignes par fichier
  df_by_file = pd.DataFrame(columns=df_res_copy.columns) #créer un nouveau dataframe
  p = 0
  df_of_top=pd.DataFrame(columns=df_res_copy.columns)
  for key,item in df_res_copy_grouped: #parcourir les groupes
    p = p+1
    a_group = df_res_copy_grouped.get_group(key) #trouver les lignes du groupe
    #find the three max scores
    top_three = a_group['norm_score'].nlargest(3)
    
    p = 0
    for i in top_three.index.values:
      p = p+1
      row = a_group.loc[i,["folder", "question","answer","norm_score","context","score","N"]]
      df_of_top=df_of_top.append(row)
  

  return df_of_top

