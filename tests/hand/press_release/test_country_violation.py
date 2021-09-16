# from legal_doc_processing.press_release.country_of_violation.predict import (
#     predict_country_of_violation,
# )

from geopy.geocoders import Nominatim

from legal_doc_processing import logger
from country_list import countries_for_language



from legal_doc_processing.press_release.country_of_violation.countries_list import (
    countries_list,
)

from legal_doc_processing.utils import get_spacy, get_pipeline

from legal_doc_processing.press_release.press_release import press_release_df


from legal_doc_processing.press_release.country_of_violation.predict import (
    predict_country_of_violation, clean_answer
)



# spa and pipe
nlpsa, nlpipe = get_spacy(),get_pipeline()

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
real_countries=clean_answer(countries)
countries = dict(countries_for_language('en'))
list_countries=list(countries.values())

for country in real_countries:
    assert real_countries in list_countries









from country_list import countries_for_language
try:
    # countries_for_language returns a list of tuples now, might be changed to an OrderedDict
    _countries = dict(countries_for_language('en'))

    list_countries=list(_countries.values())


    country_violation=clean_answer( list_countries)
    #tester sur un dizaine de cas
    #filtrer et ajouter une fonction de clearning
except Exception as e:
    print(e)