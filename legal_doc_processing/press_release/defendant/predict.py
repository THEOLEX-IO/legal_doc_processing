#from utils_defendant import *
from legal_doc_processing.press_release.defendant.defendant import utils_defendant

def predict_defendant (data: dict) -> list:
  text=  data.raw_text
  folder= data.source


  df_res = pd.DataFrame(columns=["folder","N","tag","question","answer","score","context","start","end","chosen"]) #le dataframe à remplir et exporter en excel
  for N in ["All"]:
    liste = text.split("\n")[:] if N=="All" else text.split("\n")[:N] #les N premières lignes du texte
    texte_tiny = "\n".join([elt for elt in liste if elt]) #les N premières lignes non vides du texte
    questions = get_questions(text)
    for question,tag in questions: 
      res = nlp2(question=question,context=texte_tiny) #detection de la reponse dans le texte
      try:
        context = texte_tiny[max(0,res.get("start")-60):min(res.get("end")+40,len(text))] #bout de texte contenant la reponse
        # ajouter une ligne au dataframe
        df_res = df_res.append({"folder":folder,"tag":tag,"question":question,"N":N,"answer":res['answer'],"score":res.get('score'),"context":context,"start":res.get('start'),"end":res.get('end')},ignore_index=True)
      except:
        #ajouter une ligne au dataframe
        df_res.append({"folder":folder,"tag":tag,"question":question,"N":N,"answer":"---","score":"---","context":"---","start":"---","end":"---"},ignore_index=True)

  df_of_top= best_predict(df_res)
  l= give_answer(df_of_top)
  return l
