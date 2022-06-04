from utils_defendant import *

def give_answer(df_of_top):

  liste= []
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
      u= _del_dummy_breaklines(s)
      u= _del_bouble_breaks_and_spaces (u)
      liste.append(u)
      i+=1
  liste = _u(liste)
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
  #df_new #un affichage


  #ajout de la colonne norme_score
  df_res_copy['norm_score'] = np.nan
  for i in range(len(df_res_copy)):
  #get question and compute weight
    question = df_res_copy.loc[i,"question"]
    weight = _get_weight(question)
    # weight=0 for answer containing defendant
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
    #if p==1: break
    p = p+1
    #get all q&a on that folder
    a_group = df_res_copy_grouped.get_group(key) #trouver les lignes du groupe
    #find the three max scores
    top_three = a_group['norm_score'].nlargest(1)
    
    p = 0
    for i in top_three.index.values:
      p = p+1
      row = a_group.loc[i,["folder", "question","answer","norm_score","context","score","N"]]
      df_of_top=df_of_top.append(row)
  

  return df_of_top


def predict_defendant (data: dict) -> list:
  text= "\n".join(data[key] for key in data.keys())
  folder= data["source"]


  df_res = pd.DataFrame(columns=["folder","N","tag","question","answer","score","context","start","end","chosen"]) #le dataframe à remplir et exporter en excel
  for N in ["All"]:
    #print(", \n>>>>N = ",N)
    liste = text.split("\n")[:] if N=="All" else text.split("\n")[:N] #les N premières lignes du texte
    texte_tiny = "\n".join([elt for elt in liste if elt]) #les N premières lignes non vides du texte
    questions = get_questions(text)
    for question,tag in questions: 
      res = nlp2(question=question,context=texte_tiny) #detection de la reponse dans le texte
      #print(tag,res) #quick print
      try:
        context = texte_tiny[max(0,res.get("start")-60):min(res.get("end")+40,len(text))] #bout de texte contenant la reponse
        #print("context: ",context,end="\n\n") #quick print
        # ajouter une ligne au dataframe
        df_res = df_res.append({"folder":folder,"tag":tag,"question":question,"N":N,"answer":res['answer'],"score":res.get('score'),"context":context,"start":res.get('start'),"end":res.get('end')},ignore_index=True)
      except: #si il y a un problème
        #print("a pb",end="\n\n") #quick print
        #ajouter une ligne au dataframe
        df_res.append({"folder":folder,"tag":tag,"question":question,"N":N,"answer":"---","score":"---","context":"---","start":"---","end":"---"},ignore_index=True)

  df_of_top= best_predict(df_res)
  l= give_answer(df_of_top)
  return l