from legal_doc_processing.press_release.decision_date.predict import predict_decision_date


from geopy.geocoders import Nominatim

from legal_doc_processing.press_release.press_release import press_release_df
from legal_doc_processing.utils import get_label_, get_spa_pipe




# spa and pipe
nlpsa, nlpipe = get_spa_pipe()

# make df
df = press_release_df(
    "doj",
    nlpipe=nlpipe,
    nlspa=nlpsa,
    sample=0.25,
)

pr = df.pr.iloc[10]
pr.predict("extracted_authorities")
data = pr.data

predict_decision_date(data)
