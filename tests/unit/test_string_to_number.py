from tests import *

from legal_doc_processing.press_release.information_extraction.cost import (
    _string_to_number,
)


class TestStringToNumber(unittest.TestCase):
    """ """

    def test_millions(self):

        text_list = [("1.3 millions of dollars", 1_300_000), ("$1,000,000", 1_000_000)]
        cands = [i[0] for i in text_list]
        y = [str(i[1] for i in text_list)]

        preds = _string_to_number(cands)
        ans = list(zip(preds, y))
        accuracy = [i == j for i, j in ans]
