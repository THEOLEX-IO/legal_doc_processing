from tests import *
from document_processing import information_extraction


class TestInformationExtraction(unittest.TestCase):

    def test_docket_case_1(self):
        self.assertEqual(information_extraction.get_case(["CFTC Docket NO. SD 20-01"]), 'NO. SD 20-01')



