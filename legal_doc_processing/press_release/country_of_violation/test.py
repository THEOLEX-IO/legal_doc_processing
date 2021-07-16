# from legal_doc_processing.press_release.country_of_violation.predict import (
#     predict_country_of_violation,
# )


# from transformers import (
#     pipeline,
#     AutoModelForTokenClassification,
#     AutoTokenizer,
#     AutoModelForQuestionAnswering,
# )

# from geopy.geocoders import Nominatim

# # ask question about the residence of the defendant
# [
#     "where is the person who is charge from?",
#     "Where does the person who is charge from",
#     "Where is the country of violation?",
# ]


# geolocator = Nominatim(user_agent="geoapiExercises")
# location = geolocator.geocode("Dakar")

# location._address

import pdb

from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import get_label_

from legal_doc_processing.press_release.country_of_violation.countries_list import (
    countries_list,
)


def predict_country_of_violation(data: dict) -> list:
    """ """

    # authorities list
    juridiction = data.juridiction
    auth_list = data.feature_dict["extracted_authorities"].lower().split(";;")

    # TO BE VALIDATED WITH MARTINE CFPB & CFTC --> 99 % accuracy USA
    # cfbp and cftc -> USA
    for auth in ["cfbp", "cftc"]:
        if juridiction in auth:
            return [("United States", 1)]

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents

    # find the list of countries
    countries_cands = list()
    for sent in sent_list:
        # find GPE
        cand = get_label_(sent, "GPE", data.nlspa)
        # extend countries_cands
        countries_cands.append([sent, cand])

    # clean empty GPE item
    countries_cands = [[i, j] for i, j in countries_cands if j]

    ans_list = list()
    for sent, country in countries_cands:
        quest = [["where does the violation took place?", "fine"]]
        
        ans = ask_all(sent, quest, sent=sent, sent_id=country, nlpipe=data.nlpipe)
        ans_list.extend(ans)

    ans_list=sorted(ans_list, key=lambda i: i["score"], reverse=True)
    is_good=lambda answer, sent_id: any([i for i in sent_id if i in answer.strip()])
    ans_list= [i for i in ans_list if is_good(i["answer"], i["sent_id"])]





    # countries_lowered = _u([i.lower().strip() for i in countries_cands])

    # # filter
    # _countries_list = [i.lower().strip() for i in countries_list]
    # in_countries = lambda i: i.replace("the", "").strip() in _countries_list
    # countries_filtered = [
    #     i.replace("the", "").strip() for i in countries_lowered if in_countries(i)
    # ]

    return ans_list

   # spa and pipe
    nlpsa, nlpipe = get_spa_pipe()

    # make df
    df = press_release_df(
        "doj",
        nlpipe=nlpipe,
        nlspa=nlpsa,
        sample=0.25,
    )

    pr = df.pr.iloc[6]
    pr.predict("extracted_authorities")
    data = pr.data

#test the prediction
countries=predict_country_of_violation(data)

#filter the prediction 
for cv in countries[0]:
     if cv["score"]>0.5:
         print(cv["answer"])





if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import get_label_, get_spa_pipe
    from legal_doc_processing.utils import ask_all

    from legal_doc_processing.press_release.press_release import press_release_df
    from legal_doc_processing.press_release import country_of_violation




def predict_country_of_violation(data: dict) -> list:
    """ """

    # authorities list
    juridiction = data.juridiction
    auth_list = data.feature_dict["extracted_authorities"].lower().split(";;")

    # cfbp and cftc -> USA
    for auth in ["cfbp", "cftc"]:
        if juridiction in auth:
            return [("United States", 1)]

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents

    # find the list of countries
    countries_cands = list()
    for sent in sent_list:
        countries_cands.extend(get_label_(sent, "GPE", data.nlspa))
    countries_lowered = _u([i.lower().strip() for i in countries_cands])

    # filter
    _countries_list = [i.lower().strip() for i in countries_list]
    in_countries = lambda i: i.replace("the ", "").strip() in _countries_list
    countries_filtered = [
        i.replace("the", "").strip() for i in countries_lowered if in_countries(i)
    ]

    # if not countries_filtered:
    # pdb.set_trace()

    return [(i, 1) for i in countries_filtered]



 

    ask_all(df.press_release_text, [("Where does the violation heppen?", "ok")], nlpipe=nlpipe)
