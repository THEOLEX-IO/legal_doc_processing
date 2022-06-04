from utils import *

def predict_monetary_sanction (data: dict) -> list:
  text= "\n".join(data[key] for key in data.keys())
  folder= data["source"]
  #On écrira ici une fonction qui prend text qui qui ressort le dataframe avec les réponses

  df_res = pd.DataFrame(columns=["folder","N","tag","question","answer","score","context","start","end","chosen"]) #le dataframe à remplir et exporter en excel
  for N in [15,20,30,"All"]:
    #print("\n>>>>N = ",N)
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
      #print(tag,res) #quick print
      try:
        context = texte_tiny[max(0,res.get("start")-60):min(res.get("end")+40,len(text))] #bout de texte contenant la reponse
        #print("context: ",context,end="\n\n") #quick print
        # ajouter une ligne au dataframe
        df_res = df_res.append({"folder":folder,"tag":tag,"question":question,"N":N,"answer":res['answer'],"score":res.get('score'),"context":context,"start":res.get('start'),"end":res.get('end')},ignore_index=True)
      except: #si il y a un problème
        #print("a pb",end="\n\n") #suick print
        #ajouter une ligne au dataframe
        df_res.append({"folder":folder,"tag":tag,"question":question,"N":N,"answer":"---","score":"---","context":"---","start":"---","end":"---"},ignore_index=True)



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
    #compute score
    score = df_res_copy.loc[i,'score']
    df_res_copy.loc[i,'norm_score'] = weight*score



  #recherche du  top et création du dataframe contenant le top3+ best normal
  log=False
  #transform df in df_grouped in order to
  df_res_copy_grouped = df_res_copy.groupby(["folder"]) #grouper les lignes par fichier
  df_by_file = pd.DataFrame(columns=df_res_copy.columns) #créer un nouveau dataframe
  p = 0
  df_of_top=pd.DataFrame(columns=df_res_copy.columns)
  for key,item in df_res_copy_grouped: #parcourir les groupes
    #if p==1: break
    #print("\n\n\n>>>>>>>>>>>>>>>>>>>>>>>",key,">>>>>>>>>>>>>>>>>>>>>>>")
    p = p+1

    #get all q&a on that folder
    a_group = df_res_copy_grouped.get_group(key) #trouver les lignes du groupe
    #if log: print(a_group[["folder","tag","question","score","norm_score"]])

    #find the three max scores
    top_three = a_group['norm_score'].nlargest(3)
    #print("\ntop three:")
    
    p = 0
    for i in top_three.index.values:
      p = p+1
      row = a_group.loc[i,["folder", "question","answer","norm_score","context","score","N"]]
      df_of_top=df_of_top.append(row)
      #print("\n>>",f"n°{p}")
      #print(row)
      #print("answer = ",row["answer"])
      #print("context = ",row["context"])
      #print("new score = ",row["norm_score"])
      #print("question = ",row["question"],">>N :",row["N"])
      #print("previous score = ",row["score"])
  
    #print("\n>>best_prev")
    slice_onN_all = a_group
    old_best_row = slice_onN_all[slice_onN_all["score"]==np.max(slice_onN_all["score"])]
    df_of_top=df_of_top.append(old_best_row)
    #print("score = ",list(old_best_row["score"])[0])
    #print("answer = ",list(old_best_row["answer"])[0])
    #print("context = ",list(old_best_row["context"])[0])
    #print("question = ",list(old_best_row["question"])[0],">>N :",list(old_best_row["N"])[0])
    
    #if log: print("\nmax = ",np.max(a_group["norm_score"]))
    best_row = a_group[a_group["norm_score"]==np.max(a_group["norm_score"])]
    #if log: print("best row = ",best_row)

    #print("answer = ",list(best_row["answer"])[0])
    #print("context = ",list(best_row["context"])[0])
    #print("question = ",list(best_row["question"])[0])
    df_by_file = df_by_file.append(best_row) #ajouter les lignes au nouveau dataframe
  #df_by_file #un affichage 

  #extract to excel
  #df_by_file.to_excel('df_by_file.xlsx')



  #on choisit finalement l'élément adapté
  df_of_topp = df_of_top.groupby(["folder"])
  l= pd.DataFrame(columns=["fichier", "answer", "context", "score"])
  for key,item in df_of_topp:
    fichiers = df_of_topp.get_group(key)
    fichiers = fichiers.reset_index(drop=True)
    l2=[]
    l1=[]
    longueur=len(fichiers)
    #print (fichiers)
    #print("----------------------------------------")
    i=0
    while (i < longueur):
      line=fichiers.loc[i, ["folder", "answer", "context", "score"]]
      t=fichiers.at[i, 'answer']
      s=str(t)
      #print(type(s))
      #print(t)
      v=s.find("$")
      #print(v)
      if (v==-1):
        fichiers=fichiers.drop(fichiers.index[i])
        #print(df)
        #print("______________________________________________________________________________")
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
  final_result= [] 
  final_result.append(l.loc[0,"answer"]) 
  return final_result