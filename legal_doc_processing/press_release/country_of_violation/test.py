from legal_doc_processing.press_release.country_of_violation.predict import predict_country_of_violation






from geopy.geocoders import Nominatim

 
geolocator = Nominatim(user_agent = "geoapiExercises")
location = geolocator.geocode("California")

location._address