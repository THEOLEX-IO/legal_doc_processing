#from utils import *
from legal_doc_processing.press_release.monetary_sanction.monetary_sanction import utils_monetary_sanction

def predict_monetary_sanction (data: dict) -> list:
  #text= "\n".join(data[key] for key in data.keys())
  text= data.raw_text
  folder= data.source
  #On écrira ici une fonction qui prend text qui qui ressort le dataframe avec les réponses

  df_res = pd.DataFrame(columns=["folder","N","tag","question","answer","score","context","start","end","chosen"]) #le dataframe à remplir et exporter en excel
  for N in [15,20,30,"All"]:
    liste = text.split("\n")[:] if N=="All" else text.split("\n")[:N] #les N premières lignes du texte
    texte_tiny = "\n".join([elt for elt in liste if elt]) #les N premières lignes non vides du texte
    questions = [("How much is ordered to pay as monetary sanction?", "pay_order"),
            ("How much is restituate?", "much_restituate"),
            ("How much is the monetary sanction?", "how_monetary"),
            ("What is ordered to pay?", "what_order"),
            ("what is restituate?", "what_restituate")
            ]
    for question,tag in questions: 
      res = nlp2(question=question,context=texte_tiny) #detection de la reponse dans le texte
      try:
        context = texte_tiny[max(0,res.get("start")-60):min(res.get("end")+40,len(text))] #bout de texte contenant la reponse
        df_res = df_res.append({"folder":folder,"tag":tag,"question":question,"N":N,"answer":res['answer'],"score":res.get('score'),"context":context,"start":res.get('start'),"end":res.get('end')},ignore_index=True)
      except: #si il y a un problème
        df_res.append({"folder":folder,"tag":tag,"question":question,"N":N,"answer":"---","score":"---","context":"---","start":"---","end":"---"},ignore_index=True)



  #transform df in df_grouped in order to display together result for different N
  df_res_grouped = df_res.groupby(["folder","tag","question"]) #grouper les lignes par fichier et question
  df_res_copy = pd.DataFrame(columns=df_res.columns) #créer un nouveau dataframe
  for key,item in df_res_grouped: #parcourir les groupes
    a_group = df_res_grouped.get_group(key) #trouver les lignes du groupe
    df_res_copy = df_res_copy.append(a_group) #ajouter les lignes au nouveau dataframe

  #ajout de la colonne norme_score
  df_res_copy['norm_score'] = np.nan
  for i in range(len(df_res_copy)):
  #get question and compute weight
    question = df_res_copy.loc[i,"question"]
    weight = _get_weight(question)
    # weight=0 for answer containing defendant
    answer = df_res_copy.loc[i,"answer"]
    folder = df_res_copy.loc[i,"folder"]
    #compute score
    score = df_res_copy.loc[i,'score']
    df_res_copy.loc[i,'norm_score'] = weight*score

  #recherche du  top et création du dataframe contenant le top3+ best normal
  log=False
  df_res_copy_grouped = df_res_copy.groupby(["folder"]) #grouper les lignes par fichier
  df_by_file = pd.DataFrame(columns=df_res_copy.columns) #créer un nouveau dataframe
  p = 0
  df_of_top=pd.DataFrame(columns=df_res_copy.columns)
  for key,item in df_res_copy_grouped: #parcourir les groupes
    p = p+1

    #get all q&a on that folder
    a_group = df_res_copy_grouped.get_group(key) #trouver les lignes du groupe
  
    #find the three max scores
    top_three = a_group['norm_score'].nlargest(3)

    
    p = 0
    for i in top_three.index.values:
      p = p+1
      row = a_group.loc[i,["folder", "question","answer","norm_score","context","score","N"]]
      df_of_top=df_of_top.append(row)

    slice_onN_all = a_group
    old_best_row = slice_onN_all[slice_onN_all["score"]==np.max(slice_onN_all["score"])]
    df_of_top=df_of_top.append(old_best_row)

    best_row = a_group[a_group["norm_score"]==np.max(a_group["norm_score"])]
    df_by_file = df_by_file.append(best_row) #ajouter les lignes au nouveau dataframe



  #on choisit finalement l'élément adapté
  df_of_topp = df_of_top.groupby(["folder"])
  l= pd.DataFrame(columns=["fichier", "answer", "context", "score"])
  for key,item in df_of_topp:
    fichiers = df_of_topp.get_group(key)
    fichiers = fichiers.reset_index(drop=True)
    l2=[]
    l1=[]
    longueur=len(fichiers)
    i=0
    while (i < longueur):
      line=fichiers.loc[i, ["folder", "answer", "context", "score"]]
      t=fichiers.at[i, 'answer']
      s=str(t)
      v=s.find("$")
      if (v==-1):
        fichiers=fichiers.drop(fichiers.index[i])
        i=0
      else:
        i+=1
        l2.append(s)
      longueur=len(fichiers)
      fichiers = fichiers.reset_index(drop=True)
    l1= _cast_as_int(l2)
    if len(l1)==0:
      l=l.append(line)
    else:
      index_max=l1.index(max(l1))
      row=fichiers.loc[index_max, ["folder", "answer", "context", "score"]]
      l=l.append(row)
  l = l.reset_index ()
  final_result= [] 

  if (len(l)!=0):
    final_result.append(l.loc[0,"answer"])
  else:
    final_result.append(str(0))
  final_result= _cast_as_int(final_result)
  if ((len(final_result)) ==0):
    final_result.append(str(0))

  return final_result


#     """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

#     # pipe, spa
#     nlpipe, nlspa = data.["nlpipe"], data.["nlspa"]
