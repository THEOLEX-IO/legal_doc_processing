from legal_doc_processing.press_release.country_of_violation.predict import clean_answer
from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all, cosine_similarity
from legal_doc_processing.press_release.defendant.questions import (
    _question_helper,
    _question_selector,
    _question_lister,
)
from legal_doc_processing.press_release.defendant.clean import (
    _sub_you_shall_not_pass,
    clean_ans,
)

def correct_context(data):
    possible_words=['monetary', 'money', 'sanction', 'monetary sanction', 'ordered', 'pay', 'defendant']
    text=[]

    if 'page' in  data.content:
        list_pages = data.content.split('page')
        for j in list_pages:
            for word in possible_words:
                if word in j:
                    if j not in text:
                        text.append(j) 
    else:
        text.append( data.content)
    col=''.join(text)
    data.content=col
    return data



def predict_defendant(
    data: dict,
    h1_len_threshold: int = 20,
    content_n_sents_threshold: int = 25,
    threshold: float = 0.5,
) -> list:
    """ """
    
    data=correct_context(data)
    # quest
    ans_list = []
    key_list = _question_helper(data.content)
    if key_list:
        quest_pairs = _question_lister(key_list)
        ans_list.extend(ask_all(data.content, quest_pairs, sent=data.content, nlpipe=data.nlpipe))
    score=[]
    for an in ans_list:
        
        if an['answer'] not in score and an['score']>threshold:
             score.append([an['answer'],an['score']] )
        else:
            score.append(["", 0])


    
    return score[0][0]
