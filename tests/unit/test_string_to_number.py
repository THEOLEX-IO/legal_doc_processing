from tests import *

from legal_doc_processing.press_release.information_extraction.cost import (
    _string_to_number,
)


class TestStringToNumber(unittest.TestCase):
    """ """

    def test_millions(self):

        text_list = [
            ("130 millions of dollars", 130_000_000),
            ("$3 000 thousand", 3_000_000),
            ("1.3 millions of dollars", 1_300_000),
            ("1,3 millions of dollars", 1_300_000),
            ("$1,000,000", 1_000_000),
            ("$1 000 000", 1_000_000),
            ("$1.000.000", 1_000_000),
            ("300000", 300_000),
            ("300 000", 300_000),
            ("300,000", 300_000),
            ("300.000", 300_000),
            ("300 thousands", 300_000),
            ("$3 thousands", 3_000),
            ("$1000", 1_000),
            ("$1 000", 1_000),
            ("$1,000", 1_000),
            ("$1thousand", 1_000),
        ]
        # cands = [i[0] for i in text_list]
        # y = [int(i[1]) for i in text_list]

        cands, y = list(zip(*text_list))

        preds = _string_to_number(cands)
        ans = list(zip(preds, y))
        accuracy = sum([i == j for i, j in ans]) / len(ans)
        assert accuracy > 0.99
