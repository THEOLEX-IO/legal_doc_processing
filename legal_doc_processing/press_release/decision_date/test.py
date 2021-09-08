from datetime import datetime
from legal_doc_processing.press_release.decision_date.predict import predict_decision_date
from legal_doc_processing.utils import get_label_, get_pipeline, get_spacy
from legal_doc_processing.press_release.press_release import press_release_df
import pytest


def test_predict_date():

    nlpsa, nlpipe = get_spacy(), get_pipeline()

    # make df
    df = press_release_df(
        
        nlpipe=nlpipe,
        nlspa=nlpsa,
        
        sample=0.1,
    )
    pr = df.pr.iloc[0]
    pr.predict("extracted_authorities")
    data = pr.data

    assert int(predict_decision_date(data)[0][0].split("-")[0]) in range(1900,2020) or predict_decision_date(data)[0][0].split("-")[0]==""
