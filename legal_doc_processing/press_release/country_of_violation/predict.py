import pdb
import numpy as np

from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import get_label_, ask_all

from legal_doc_processing.press_release.country_of_violation.countries_list import (
    countries_list,
)


from country_list import countries_for_language
from geopy.geocoders import Nominatim




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
    countries_cands = []
    for sent in sent_list:
        # find GPE
        cand = get_label_(sent, "GPE", data.nlspa)
        # extend countries_cands
        countries_cands.append([sent, cand])

    # clean empty GPE item
    countries_cands = [[i, j] for i, j in countries_cands if j]

    ans_list = []
    for sent, country in countries_cands:
        quest = [["What is the country of violation?", "fine"]]

        ans = ask_all(sent, quest, sent=sent, sent_id=country, nlpipe=data.nlpipe)
        ans_list.extend(ans)

    ans_list = sorted(ans_list, key=lambda i: i["score"], reverse=True)
    is_good = lambda answer, sent_id: any(i for i in sent_id if i in answer.strip())
    ans_list = [(i["answer",i["score"]])for i in ans_list if is_good(i["answer"], i["sent_id"])]

    # countries_lowered = _u([i.lower().strip() for i in countries_cands])

    # # filter
    # _countries_list = [i.lower().strip() for i in countries_list]
    # in_countries = lambda i: i.replace("the", "").strip() in _countries_list
    # countries_filtered = [
    #     i.replace("the", "").strip() for i in countries_lowered if in_countries(i)
    # ]

    # return [(i, 1) for i in countries_filtered]

    return ans_list


def clean_answer(answer_disc):
    list_answer=[]
    cleaned_countries=[]
    country_violation=[]

    for cv in answer_disc:
        if cv[1] > 0.7:
            list_answer.append(cv)
    if len(list_answer)!=0:
        for i in range(len(list_answer)):
            country=list_answer[i][0].lower().split(",")
        # print("here country",country)
            if "district"!=country:
                cleaned_countries.append(list_answer[i])


    _countries = dict(countries_for_language('en'))

    list_countries=list(_countries.values())
#select all the country from the answers
    if list_countries:
        for country in cleaned_countries:
            if country[0] in list_countries:
                country_violation.append(country)

        #convert the cities into country
            else:
                geolocator = Nominatim(user_agent="geoapiExercises")
                location=geolocator.geocode(country[0])
                if location:
                    country_violation.append(tuple(location.address.split(",")[-1], country[1]))


    
    
    return answer_disc
