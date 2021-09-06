import pytest
from legal_doc_processing.press_release.press_release import  press_release_df




def test_string_method():
    """
    test if montetary sanction predict return only string
    """

    df=press_release_df(
        
        sample=0.25,

    )

    df["monetary_sanction"]= df.pr.apply(lambda i: i.predict('monetary_sanction'))
    assert df.monetary_sanction[0][0]==str




