from transformers import pipeline
nlp2 = pipeline("question-answering")
import os
import pandas as pd

def predict_decision_date (data: dict) -> list:
  text= "\n".join(data[key] for key in data.keys())
  folder= data["source"]
  final_result =[]
  df_res = pd.DataFrame(columns=["folder","N","tag","question","answer","score","context","start","end","chosen"]) #le dataframe à remplir (au cas où)
  N =20
  liste = text.split("\n")[:N] #les N premières lignes du texte
  texte_tiny = "\n".join([elt for elt in liste if elt]) #les N premières lignes non vides du texte
  questions = [("what is the date?", "what_date")]
  for question,tag in questions: 
    res = nlp2(question=question,context=texte_tiny) #detection de la reponse dans le texte
    s = res['answer']
    final_result.append(s)
    try:
      context = texte_tiny[max(0,res.get("start")-60):min(res.get("end")+40,len(text))] #bout de texte contenant la reponse
      df_res = df_res.append({"folder":folder,"tag":tag,"question":question,"N":N,"answer":res['answer'],"score":res.get('score'),"context":context,"start":res.get('start'),"end":res.get('end')},ignore_index=True)
    except: #si il y a un problème
      df_res.append({"folder":folder,"tag":tag,"question":question,"N":N,"answer":"---","score":"---","context":"---","start":"---","end":"---"},ignore_index=True)

  return final_result