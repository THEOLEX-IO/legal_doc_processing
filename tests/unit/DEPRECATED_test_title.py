from tests import *
from legal_doc_processing import utils


class TestTitle(unittest.TestCase):

    def test_romans_numbers(self):
        self.assertTrue(utils.is_section_num("IV."))

    def test_not_number(self):
        self.assertFalse(utils.is_section_num("lp"))


class TestPunctuation(unittest.TestCase):

    def test_punc(self):
        self.assertTrue(utils.ends_with_ponc("is ending with punc."))

    def test_not_punc(self):
        self.assertFalse(utils.ends_with_ponc("is not ending with punc"))