#import pytest
import unittest

from legal_doc_processing.press_release.press_release import press_release_df



class TestingClass(unittest.TestCase):

    def test_string_method(self):
        """
        test if montetary sanction predict return only string
        """

        df=press_release_df(
            "cftc",
            
            sample=0.25,
        )

        df["monetary_sanction"]= df.pr.apply(lambda i: i.predict('monetary_sanction'))
        df['monetary_sanction'].apply(lambda i: type(i[0]) is str)


# unittest.main()




