from datetime import date

from tests import *
from tests.helpers import *


class TestCleanDoc(unittest.TestCase):

    def test_helper(self):
        self.assertEqual(MyHelper.days_ago(date.today()), 0)

    def test_other_helper(self):
        if not tests_helper.list_has(3, [1, 2, 3]):
            raise AssertionError

    @pytest.mark.xfail
    def test_should_fail(self):
        self.assertEqual(False, True)
