from legal_doc_processing.press_release.country_of_violation.predict import predict_country_of_violation




from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer, AutoModelForQuestionAnswering

from geopy.geocoders import Nominatim

#ask question about the residence of the defendant
["where is the person who is charge from?",
"Where does the person who is charge from",
"Where is the country of violation?",
]



geolocator = Nominatim(user_agent = "geoapiExercises")
location = geolocator.geocode("Dakar")

location._address