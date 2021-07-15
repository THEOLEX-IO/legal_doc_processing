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


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import get_label_, get_spa_pipe
    from legal_doc_processing.utils import ask_all

    from legal_doc_processing.press_release.press_release import press_release_df

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
