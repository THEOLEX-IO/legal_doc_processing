from tests import *
from legal_doc_processing import information_extraction


class TestInformationExtraction(unittest.TestCase):
    def test_docket_case_1(self):
        self.assertEqual(
            information_extraction.get_case(["CFTC Docket NO. SD 20-01"]), "SD 20-01"
        )
        self.assertEqual(
            information_extraction.get_case(["the case is 12132-CV-1211"]),
            "12132-CV-1211",
        )