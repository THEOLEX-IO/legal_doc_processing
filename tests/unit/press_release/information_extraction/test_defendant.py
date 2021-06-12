from legal_doc_processing.press_release.information_extraction.defendant import (
    _clean_LLC_trailling_dot_comma,
    _clean_and,
    _clean_resident,
    _clean_defendants,
    _you_shall_not_pass,
)


class Test_clean_LLC_trailling_dot_comma(unittest.TestCase):
    """Test Class for LLC """

    def test_ok(self):
        """test succed """

        cands = [
            ("A Gaz LLC", "A Gaz"),
            ("A Gaz, LLC.", "A Gaz"),
            ("A Gaz, LLC", "A Gaz"),
        ]
        X, y = zip(*cands)

        preds = [_clean_LLC_trailling_dot_comma(x) for x in X]

        res = list(zip(X, y, preds))
        eqs = [(i == j) for i, j in zip(y, preds)]
        acc = sum(eqs) / len(eqs)
        assert acc > 0.9


class Test_clean_and(unittest.TestCase):
    """Test Class and"""

    def test_ok(self):
        """test succeed """

        cands = [
            (["Alex and Lucy"], ["Alex", "Lucy"]),
        ]
        X, y = zip(*cands)

        preds = [_clean_and(x) for x in X]

        res = list(zip(X, y, preds))
        eqs = [(i == j) for i, j in zip(y, preds)]
        acc = sum(eqs) / len(eqs)
        assert acc > 0.9


class Test_clean_and(unittest.TestCase):
    """Test Class and"""

    def test_ok(self):
        """test succeed """

        cands = [
            (["Alex and Lucy"], ["Alex", "Lucy"]),
        ]
        X, y = zip(*cands)

        preds = [_clean_and(x) for x in X]

        res = list(zip(X, y, preds))
        eqs = [(i == j) for i, j in zip(y, preds)]
        acc = sum(eqs) / len(eqs)
        assert acc > 0.9


class Test_clean_resident(unittest.TestCase):
    """Test Class _clean_resident"""

    def test_ok(self):
        """test succeed """

        cands = [
            ("Alex Gazagnes", "Alex Gazagnes"),
            ("Rouen Resident Alex Gazagnes", "Alex Gazagnes"),
            ("former Resident Alex Gazagnes", "Alex Gazagnes"),
        ]

        X, y = zip(*cands)

        preds = [_clean_resident(x) for x in X]

        res = list(zip(X, y, preds))
        eqs = [(i == j) for i, j in zip(y, preds)]
        acc = sum(eqs) / len(eqs)
        assert acc > 0.9


class Test_clean_defendants(unittest.TestCase):
    """ """

    def test_ok(self):
        """ """

        cands = ans_list = [
            ("defendant Alex Gazagnes", "Alex Gazagnes"),
            ("Defendants Alex Gazagnes", "Alex Gazagnes"),
        ]

        X, y = zip(*cands)

        preds = _clean_defendants(X)

        res = list(zip(X, y, preds))
        eqs = [(i == j) for i, j in zip(y, preds)]
        acc = sum(eqs) / len(eqs)
        assert acc > 0.9


class Test_you_shall_not_pass(unittest.TestCase):
    """Test Class_you_shall_not_pass"""

    def test_ok(self):
        """test succeed """

        ans_list = X = [
            "defendant",
            "defendants",
            "ejidej deznuindniinin nuin",
            "hduehizhdiheihifzeifhihihefhifuhiehueih uheiz hfuihfuize huizeh uifhuifhzeuhf uizhfuieh zehfzu hizehu eizhf izuh",
            "hduehizhdiheihifzeifhihihefhifuhiehueih uhe, hfuihfuize huizeh uifhuifhzeuhf uizhfuieh zehfzu hizehu eizhf izuh",
            "Alex Gazagnes LLC",
            "Alex Gazagnes LLC",
            "Alex Gazagnes, Ltd.",
            "   Rouen Resident Alex Gazagnes   ",
            "former Resident Alex Gazagnes",
            "defendant Alex Gazagnes",
            "Alex Gazagnes and John Doe",
            "AlexI Gazagnes, JohnI Doe LLC.",
            "AlexA Gazagnes, JohnA Doe LLC.",
            "Alex Gazagnes, LLC. and John Doe LLC.",
            "AlexI Gazagnes, LLC. and JohnI Doe LLC.",
            "societe international LLC, Alex Gazagnes, John Doe and Fran Fine",
        ]

        y = [
            "Alex Gazagnes",
            "John Doe",
            "AlexI Gazagnes",
            "JohnI Doe",
            "AlexA Gazagnes",
            "JohnA Doe",
            "societe international,  Fran Fine",
        ]

        preds = [_you_shall_not_pass(x) for x in X]

        res = list(zip(X, y, preds))
        eqs = [(i == j) for i, j in zip(y, preds)]
        acc = sum(eqs) / len(eqs)
        assert acc > 0.9
