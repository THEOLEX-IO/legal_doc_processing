# from legal_doc_processing.press_release.country_of_violation.predict import (
#     predict_country_of_violation,
# )

# from transformers import (
#     pipeline,
#     AutoModelForTokenClassification,
#     AutoTokenizer,
#     AutoModelForQuestionAnswering,
# )

from geopy.geocoders import Nominatim

# # ask question about the residence of the defendant
# [
#     "where is the person who is charge from?",
#     "Where does the person who is charge from",
#     "Where is the country of violation?",
# ]

# geolocator = Nominatim(user_agent="geoapiExercises")
# location = geolocator.geocode("Dakar")

# location._address

from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import get_label_

from legal_doc_processing.press_release.country_of_violation.countries_list import (
    countries_list,
)

from legal_doc_processing.utils import get_label_, get_spa_pipe
from legal_doc_processing.utils import ask_all

from legal_doc_processing.press_release.press_release import press_release_df
from legal_doc_processing.press_release import country_of_violation


from legal_doc_processing.press_release.country_of_violation.predict import (
    predict_country_of_violation, clean_answer
)


from geopy.geocoders import Nominatim

# spa and pipe
nlpsa, nlpipe = get_spa_pipe()

# make df
df = press_release_df(
    "doj",
    nlpipe=nlpipe,
    nlspa=nlpsa,
    sample=0.25,
)

pr = df.pr.iloc[0]
pr.predict("extracted_authorities")
data = pr.data

# test the prediction
countries = predict_country_of_violation(data)
ans_list = sorted(countries, key=lambda i: i["score"], reverse=True)
is_good = lambda answer, sent_id: any([i for i in sent_id if i in answer.strip()])
ans_list = [i for i in ans_list if is_good(i["answer"], i["sent_id"])]

# filter the prediction
for cv in ans_list:
    if cv["score"] > 0.5:
        print(cv["answer"])






from country_list import countries_for_language
# countries_for_language returns a list of tuples now, might be changed to an OrderedDict
_countries = dict(countries_for_language('en'))

list_countries=list(_countries.values())


country_violation=clean_answer(countries)
#tester sur un dizaine de cas
#filtrer et ajouter une fonction de clearning