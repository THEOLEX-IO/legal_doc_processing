from tests import *

from legal_doc_processing.press_release.monetary_sanction.clean import _cast_as_int


class TestCastAsInt(unittest.TestCase):
    """ """

    def test_cast_as_int(self):
        def _test_cast_as_int():

            text_list = [
                ("hundred of million of dollars", 100_000_000),
                ("a total amount of 75 millions of dollars", 75_000_000),
                ("130 millions of dollars", 130_000_000),
                ("the fuckingsum of $3 000 thousand", 3_000_000),
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

            X, y = list(zip(*text_list))

            preds = _cast_as_int(X)
            ans = list(zip(preds, y))
            accuracy = sum([i == j for i, j in ans]) / len(ans)
            assert accuracy > 0.90

            return list(zip(X, y, preds))

        _test_cast_as_int()
